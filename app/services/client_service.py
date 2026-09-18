import uuid
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.client_model import Client
from app.repositories.client_repository import ClientRepository
from app.schema.client_schema import CreateClientRequest


class ClientService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = ClientRepository(db)

    def _to_response(self, client: Client) -> dict:
        return {
            "id": str(client.id),
            "name": client.name,
            "email": client.email,
            "phone": client.phone,
            "company_name": client.company_name,
            "is_active": client.is_active,
        }

    async def create(self, request: CreateClientRequest) -> dict:
        client = Client(
            name=request.name,
            email=request.email,
            phone=str(request.phone),
            company_name=request.company_name,
            is_active=True,
        )
        client = await self.repo.create(client)
        await self.db.commit()
        return {"success": True, "message": "Client created.", "client": self._to_response(client)}

    async def get_all(self) -> dict:
        clients = await self.repo.get_all()
        return {
            "success": True,
            "total": len(clients),
            "clients": [self._to_response(c) for c in clients],
        }

    async def get_by_id(self, client_id: uuid.UUID) -> dict:
        client = await self.repo.get_by_id(client_id)
        if not client:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
        return self._to_response(client)

    async def update(self, client_id: uuid.UUID, data: dict) -> dict:
        client = await self.repo.get_by_id(client_id)
        if not client:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
        for key, value in data.items():
            if value is not None:
                setattr(client, key, value)
        client = await self.repo.update(client)
        await self.db.commit()
        return {"success": True, "message": "Client updated.", "client": self._to_response(client)}

    async def delete(self, client_id: uuid.UUID) -> dict:
        client = await self.repo.get_by_id(client_id)
        if not client:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
        await self.repo.delete(client)
        await self.db.commit()
        return {"success": True, "message": "Client deleted successfully."}
