from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.team_service import TeamService
from app.common.deps import get_manager_user, get_db
from app.schema.team_schema import AssignTeamRequest, AssignTeamResponse
from app.services.team_service import TeamService



router = APIRouter(prefix="/assign", tags=["Assign Team"])


@router.post("/team", response_model=AssignTeamResponse, status_code=status.HTTP_201_CREATED)
async def create_team(
    request: AssignTeamRequest, 
    current_user= Depends(get_manager_user), 
    db: AsyncSession = Depends(get_db)
):
    service = TeamService(db)   
    return await service.assign_team(request)










