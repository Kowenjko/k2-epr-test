from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Order, OrderItem


class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, order_id: int) -> Order | None:
        result = await self.session.execute(
            select(Order)
            .where(Order.id == order_id)
            .options(
                selectinload(Order.items).selectinload(OrderItem.product),
                selectinload(Order.client),
            )
        )
        return result.scalar_one_or_none()

    async def get_by_client(self, client_id: int) -> list[Order]:
        result = await self.session.execute(
            select(Order)
            .where(Order.client_id == client_id)
            .options(
                selectinload(Order.items).selectinload(OrderItem.product),
                selectinload(Order.client),
            )
            .order_by(Order.created_at.desc())
        )
        return result.scalars().all()
