
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.project_model import Project
from app.models.team_model import Team
from app.models.team_member_model import TeamMember
from sqlalchemy.orm import selectinload

class ProjectRepository:
    def __init__(self, db : AsyncSession):
        self.db = db

    async def create_project(self, project: Project):
        self.db.add(project)
        await self.db.commit()
        await self.db.refresh(project)
        return project

    async def get_all_projects(self) -> list[Project]:
        result = await self.db.execute(select(Project))
        return result.scalars().all()

    async def create_team(self, team: Team):
        self.db.add(team)
        await self.db.commit()
        await self.db.refresh(team)
        return team

    async def get_all_teams(self) -> list[Team]:
        result = await self.db.execute(
            select(Team).options(selectinload(Team.members))
        )
        return result.scalars().all()

    async def get_team_by_id(self, team_id) -> Team | None:
        result = await self.db.execute(
            select(Team).options(selectinload(Team.members)).where(Team.id == team_id)
        )
        return result.scalars().first()


    # async def assign_project(self,project_id : uuid.UUID,team_id : uuid.UUID):
    #     project = await self.db.execute(select(Project).where(Project.id == project_id))
    #     project = project.scalar_one_or_none()
    #     if not project:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    #     project.team_id = team_id
    #     await self.db.commit()
    #     return project
