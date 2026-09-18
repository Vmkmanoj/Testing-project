
from app.schema.team_schema import AssignTeamRequest ,AssignTeamResponse


from app.models.team_member_model import TeamMember
from app.repositories.team_repositoty import TeamRepository

class TeamService:
    def __init__(self,db):
        self.db = db
        self.repo = TeamRepository(db)

    async def assign_team(self,request: AssignTeamRequest):

        team = TeamMember(
            user_id=request.user_id,
            team_id=request.team_id
        )

        team = await self.repo.assignTeam(team)
        await self.db.commit()

        return AssignTeamResponse(
            success=True,
            message="Team assigned successfully.",
        )

    




        
