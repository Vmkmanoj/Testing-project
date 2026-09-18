from app.models import TeamMember
from sqlalchemy.ext.asyncio import AsyncSession



class TeamRepository:
    def __init__(self, db : AsyncSession):
        self.db = db

    async def assignTeam(self, request: TeamMember):
        team = TeamMember(
            user_id=request.user_id,
            team_id=request.team_id
        )
        self.db.add(team)
        await self.db.commit()
        return team


        


        

        