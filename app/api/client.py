import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.common.deps import get_hr_user, get_authenticated_user
from app.services.client_service import ClientService
from app.schema.client_schema import CreateClientRequest

router = APIRouter(prefix="/clients", tags=["Clients"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_client(
    request: CreateClientRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_hr_user),
):
    return await ClientService(db).create(request)


@router.get("/")
async def list_clients(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_authenticated_user),
):
    return await ClientService(db).get_all()


@router.get("/{client_id}")
async def get_client(
    client_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_authenticated_user),
):
    return await ClientService(db).get_by_id(client_id)


@router.patch("/{client_id}")
async def update_client(
    client_id: uuid.UUID,
    request: dict,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_hr_user),
):
    return await ClientService(db).update(client_id, request)


@router.delete("/{client_id}", status_code=status.HTTP_200_OK)
async def delete_client(
    client_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_hr_user),
):
    return await ClientService(db).delete(client_id)
