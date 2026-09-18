from app.schema.project_schema import (
    ProjectCreate,
    CreateProjectResponse,
    AssignProjectRequest,
    AssignProjectResponse,
)
from app.models.project_model import Project
from app.repositories.project_repository import ProjectRepository
from app.schema.team_schema import CreateTeamRequest
from app.models.team_model import Team
from app.schema.team_schema import CreateTeamResponse


class ProjectService:
    def __init__(self, db):
        self.db = db
        self.repo = ProjectRepository(db)

    async def create_project(self, request: ProjectCreate):

        project = Project(
            name=request.name,
            description=request.description,
            start_date=request.start_date,
            end_date=request.end_date,
            client_id=request.client_id,
        )

        project = await self.repo.create_project(project)
        await self.db.commit()

        return CreateProjectResponse(
            success=True,
            message="Project created successfully.",
            project_id=str(project.id),
        )

    async def create_team(self, request: CreateTeamRequest):
        team = Team(name=request.name, description=request.description, project_id=request.project_id)
        team = await self.repo.create_team(team)
        await self.db.commit()

        return CreateTeamResponse(
            success=True, message="Team created successfully.", team_id=str(team.id)
        )

    async def get_all_teams(self):
        teams = await self.repo.get_all_teams()
        return [
            {
                "id": str(t.id),
                "name": t.name,
                "description": t.description,
                "project_id": str(t.project_id),
                "member_count": len(t.members),
            }
            for t in teams
        ]

    async def get_all_projects(self):
        projects = await self.repo.get_all_projects()
        return [
            {
                "id": str(p.id),
                "name": p.name,
                "description": p.description,
                "status": p.status,
                "client_id": str(p.client_id),
            }
            for p in projects
        ]


    # async def assign_project(self,request: AssignProjectRequest):
    #     project = await self.repo.assign_project(request.project_id, request.team_id)
    #     await self.db.commit()
    #     return AssignProjectResponse(
    #         success=True,
    #         message="Project assigned successfully.",
    #     )
