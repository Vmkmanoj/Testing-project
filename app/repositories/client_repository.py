import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.client_model import Client


class ClientRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, client: Client) -> Client:
        self.db.add(client)
        await self.db.flush()
        return client

    async def get_all(self) -> list[Client]:
        result = await self.db.execute(select(Client))
        return result.scalars().all()

    async def get_by_id(self, client_id: uuid.UUID) -> Client | None:
        result = await self.db.execute(
            select(Client).where(Client.id == client_id)
        )
        return result.scalars().first()

    async def update(self, client: Client) -> Client:
        self.db.add(client)
        await self.db.flush()
        return client

    async def delete(self, client: Client) -> None:
        await self.db.delete(client)
        await self.db.flush()
