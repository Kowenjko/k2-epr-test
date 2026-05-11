from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Client


class ClientRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> Client:
        result = await self.session.execute(select(Client).where(Client.email == email))
        return result.scalars().first()

    async def get_by_id(self, client_id: int) -> Client:
        result = await self.session.execute(
            select(Client).where(Client.id == client_id)
        )
        return result.scalars().first()

    async def all(self) -> list[Client]:
        result = await self.session.execute(
            select(Client).order_by(Client.created_at.desc())
        )
        return result.scalars().all()

    async def create(self, data: Client) -> Client:

        new_client = Client(**data.model_dump())
        self.session.add(new_client)
        try:
            await self.session.flush()
        except Exception:
            await self.session.rollback()
            raise

        return new_client

    async def delete(self, client: Client) -> None:
        await self.session.delete(client)
        try:
            await self.session.flush()
        except Exception:
            await self.session.rollback()
            raise
