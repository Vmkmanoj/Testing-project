from sqlalchemy.ext.asyncio import AsyncSession
from app.models.client_model import Client


class CreateEmployeeRepository:
    def __init__(self,db:AsyncSession):
        self.db = db

    async def create_client(self, client: Client) -> Client:
        self.db.add(client)
        await self.db.flush()
        return client
        