from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import ClientCreate, ClientResponse

from .repository import ClientRepository


class ClientService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = ClientRepository(session)

    async def create_client(self, client_data: ClientCreate) -> ClientResponse:
        existing_client = await self.repository.get_by_email(client_data.email)
        if existing_client:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Client with this email already exists",
            )
        new_client = await self.repository.create(client_data)
        await self.session.commit()
        return new_client

    async def get_client(self, client_id: int) -> ClientResponse:
        client = await self.repository.get_by_id(client_id)
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found",
            )
        return client

    async def all_clients(self) -> list[ClientResponse]:
        return await self.repository.all()

    async def delete_client(self, client_id: int) -> None:
        client = await self.get_client(client_id)

        await self.repository.delete(client)
        await self.session.commit()
