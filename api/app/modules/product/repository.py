from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Product


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_sku(self, sku: str) -> Product:
        result = await self.session.execute(select(Product).where(Product.sku == sku))
        return result.scalars().first()

    async def get_by_id(self, product_id: int) -> Product:
        result = await self.session.execute(
            select(Product).where(Product.id == product_id)
        )
        return result.scalars().first()

    async def get_multiple_by_ids(self, product_ids: list[int]) -> list[Product]:
        stmt = select(Product).filter(Product.id.in_(product_ids))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def all(self) -> list[Product]:
        result = await self.session.execute(
            select(Product).order_by(Product.created_at.desc())
        )
        return result.scalars().all()

    async def create(self, data: Product) -> Product:

        new_product = Product(**data.model_dump())
        self.session.add(new_product)
        try:
            await self.session.flush()
        except Exception:
            await self.session.rollback()
            raise

        return new_product

    async def delete(self, product: Product) -> None:
        await self.session.delete(product)
        try:
            await self.session.flush()
        except Exception:
            await self.session.rollback()
            raise
