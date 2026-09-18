from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.jwt import create_access_token
from app.core.password import hash_password, verify_password
from app.models.user_model import User
from app.common.enums import RoleName
from app.repositories.auth_repository import AuthRepository
from app.schema.auth_schema import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    LoginResponse,
    UserResponse,
)

from sqlalchemy import select, func

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = AuthRepository(db)

    async def login(self, request: LoginRequest) -> LoginResponse:
        user = await self.repo.get_user_by_email(request.email)

        if not user or not verify_password(request.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        # Get role name (defaults to EMPLOYEE if none assigned)
        role_name = user.roles[0].name if user.roles else RoleName.EMPLOYEE.value

        access_token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
                "role": role_name
            }
        )

        return LoginResponse(
            success=True,
            message="Login successful.",
            role=role_name,
            access_token=access_token,
            token_type="Bearer",
            user=UserResponse(
                id=str(user.id),
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                role=role_name,
            ),
        )

    async def register(self, request: RegisterRequest) -> RegisterResponse:
        existing_user = await self.repo.get_user_by_email(request.email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered.",
            )
            
        
        result = await self.db.execute(select(func.count(User.id)))
        is_first_user = result.scalar() == 0

        allowed_roles = [RoleName.EMPLOYEE.value, RoleName.MANAGER.value]
        if is_first_user:
            allowed_roles.append(RoleName.HR.value)
            
        if request.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Role must be one of: {allowed_roles}",
            )

        role = await self.repo.get_role_by_name(request.role)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Role {request.role} not found in database.",
            )

        import uuid
        manager_uuid = None
        if request.manager_id:
            if request.manager_id == "":
                manager_uuid = None
            else:
                try:
                    manager_uuid = uuid.UUID(request.manager_id)
                    manager = await self.db.get(User, manager_uuid)
                    if not manager:
                        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Assigned manager does not exist.")
                except ValueError:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid manager ID format.")

        user = User(
            first_name=request.first_name,
            last_name=request.last_name,
            email=request.email,
            password=hash_password(request.password),
            is_active=True,
            manager_id=manager_uuid,
        )

        user = await self.repo.create_user(user)
        await self.repo.assign_role_to_user(user.id, role.id)

        # Auto-create leave balances for EMPLOYEE and MANAGER
        if request.role in (RoleName.EMPLOYEE.value, RoleName.MANAGER.value):
            from app.services.leave_balance_service import LeaveBalanceService
            lb_service = LeaveBalanceService(self.db)
            await lb_service.auto_create_for_user(user.id)

        await self.db.commit()

        return RegisterResponse(
            success=True,
            message="User registered successfully.",
        )