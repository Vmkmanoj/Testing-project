from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.deps import get_manager_user, get_authenticated_user, get_db
from app.schema.project_schema import ProjectCreate, CreateProjectResponse
from app.services.project_service import ProjectService
from app.schema.team_schema import CreateTeamRequest

router = APIRouter(prefix="/project", tags=["Project"])


@router.post("/create", response_model=CreateProjectResponse)
async def create_project(
    request: ProjectCreate,
    current_user=Depends(get_manager_user),
    db: AsyncSession = Depends(get_db),
):
    service = ProjectService(db)
    return await service.create_project(request)


@router.post("/team")
async def create_team(
    request: CreateTeamRequest,
    current_user=Depends(get_manager_user),
    db: AsyncSession = Depends(get_db),
):
    service = ProjectService(db)
    return await service.create_team(request)


@router.get("/teams")
async def list_teams(
    current_user=Depends(get_authenticated_user),
    db: AsyncSession = Depends(get_db),
):
    repo = ProjectService(db)
    teams = await repo.get_all_teams()
    return {"teams": teams}


@router.get("/projects")
async def list_projects(
    current_user=Depends(get_authenticated_user),
    db: AsyncSession = Depends(get_db),
):
    repo = ProjectService(db)
    projects = await repo.get_all_projects()
    return {"projects": projects}
