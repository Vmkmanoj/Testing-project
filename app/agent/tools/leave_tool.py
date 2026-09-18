from aiohttp import client_middleware_digest_auth
from app.agent.llm import get_llm
from app.database.database import AsyncSession
from uuid import UUID
from datetime import datetime
from app.services.leave_request_service import LeaveRequestService
from app.agent.prompts.system_prompts import LEAVE_EXTRACTION_PROMPT, NAME_EXTRACTION_PROMPT
import re
import json
from app.schema.leave_request_schema import CreateLeaveRequestRequest
import uuid
from app.database.database import AsyncSessionLocal
from sqlalchemy import select
from app.models.leave_type_model import LeaveType
from app.models.leave_request_model import LeaveRequest
from app.models.user_model import User
from app.repositories.leave_balance_repository import LeaveBalanceRepository
from sqlalchemy import or_

def _llm_extract_leave_details(message: str):

    llm = get_llm()

    response = llm.invoke(LEAVE_EXTRACTION_PROMPT.format(message=message))
    text = response.content.strip()

    print("responce ", response)

    text = re.sub(r"^```(json)?|```$", "", text.strip(), flags=re.MULTILINE).strip()
    data = json.loads(text)

    print("data", data)
    
    if not isinstance(data, list):
        data = [data]
        
    requests = []
    for d in data:
        requests.append({
            "start_date": d.get("start_date"),
            "end_date": d.get("end_date") or d.get("start_date"),
            "leave_type": (d.get("leave_type") or "casual").lower(),
            "reason": d.get("reason") or "",
        })

    return requests


async def extract_leave_details(message: str) -> dict:
    print("message", message)
    if get_llm() is not None:
        try:
            return _llm_extract_leave_details(message)
        except Exception:
            pass

async def extract_employee_name(message: str) -> str | None:
    if get_llm() is not None:
        try:
            llm = get_llm()
            response = llm.invoke(NAME_EXTRACTION_PROMPT.format(message=message))
            text = response.content.strip()
            if text.lower() == "null" or not text:
                return None
            return text
        except Exception:
            return None
    return None

class LeaveTool:
    @staticmethod
    async def create_leave(
        user_id: uuid.UUID,
        start_date_str: str,
        end_date_str: str,
        leave_type_str: str,
        reason: str,
    ):
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")

        total_days = (end_date - start_date).days + 1
        if total_days <= 0:
            raise ValueError("End date must be after start date")

        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(LeaveType).where(LeaveType.name.ilike(f"%{leave_type_str}%"))
            )
            leave_type = result.scalars().first()
            if not leave_type:
                raise ValueError(f"Leave type '{leave_type_str}' not found")

            req = CreateLeaveRequestRequest(
                leave_type_id=leave_type.id,
                start_date=start_date,
                end_date=end_date,
                total_days=total_days,
                reason=reason,
            )

            service = LeaveRequestService(db)
            res = await service.create(user_id, req)

        return {
            "id": str(res.id),
            "status": res.status,
            "message": f"Successfully applied for {total_days} day(s) of {leave_type_str} leave!",
        }

    @staticmethod
    async def cancel_leave_tool(userId: str):
        try:
            user_uuid = uuid.UUID(userId)
        except ValueError:
            return {"message": "Invalid user ID format."}

        async with AsyncSessionLocal() as db:
            service = LeaveRequestService(db)
            try:
                result = await service.cancel_pending_leave_request(user_uuid)
                return {"message": result["message"]}
            except Exception as e:
                return {"message": str(e.detail if hasattr(e, 'detail') else e)}

    @staticmethod
    async def check_balance_tool(target_name: str | None, current_user_id: str):
        try:
            user_uuid = uuid.UUID(current_user_id)
        except ValueError:
            return "Invalid user ID format."

        async with AsyncSessionLocal() as db:
            target_user_id = user_uuid
            user_name_display = "You"
            
            if target_name:
                # Search for user by name
                stmt = select(User).where(
                    or_(
                        User.first_name.ilike(f"%{target_name}%"),
                        User.last_name.ilike(f"%{target_name}%")
                    )
                )
                result = await db.execute(stmt)
                user = result.scalars().first()
                
                if not user:
                    return f"Sorry, I couldn't find an employee named '{target_name}'."
                target_user_id = user.id
                user_name_display = f"{user.first_name} {user.last_name or ''}".strip()
            
            repo = LeaveBalanceRepository(db)
            year = datetime.now().year
            balances = await repo.get_by_user(target_user_id)
            
            if not balances:
                return f"{user_name_display} currently have no leave balances set up for {year}."
            
            lines = [f"Here are the leave balances for {user_name_display} ({year}):"]
            for bal in balances:
                leave_type_name = bal.leave_type.name if bal.leave_type else "Leave"
                remaining = bal.total_days - bal.used_days
                lines.append(f"- {leave_type_name}: {remaining} days remaining (out of {bal.total_days})")
                
            return "\n".join(lines)
