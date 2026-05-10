from typing import Annotated
from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from .schemas import ClientCreate, ClientResponse
from .services import ClientService

router = APIRouter(tags=["Clients"])


@router.post("/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
async def create_client(
    client_data: ClientCreate,
    session: Annotated[AsyncSession, Depends(get_db)],
):
    service = ClientService(session)
    return await service.create_client(client_data)


@router.get("/", response_model=list[ClientResponse])
async def Clients(
    session: Annotated[AsyncSession, Depends(get_db)],
):
    service = ClientService(session)
    return await service.all_clients()


@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(
    client_id: int,
    session: Annotated[AsyncSession, Depends(get_db)],
):
    service = ClientService(session)
    return await service.get_client(client_id)


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(
    client_id: int,
    session: Annotated[AsyncSession, Depends(get_db)],
):
    service = ClientService(session)
    await service.delete_client(client_id)
