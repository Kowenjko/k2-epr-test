from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import ProductCreate, ProductResponse
from .models import Product


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_sku(self, sku: str):
        result = await self.session.execute(select(Product).where(Product.sku == sku))
        return result.scalars().first()

    async def get_by_id(self, product_id: int) -> ProductResponse:
        result = await self.session.execute(
            select(Product).where(Product.id == product_id)
        )
        return result.scalars().first()

    async def all(self) -> list[ProductResponse]:
        result = await self.session.execute(
            select(Product).order_by(Product.created_at.desc())
        )
        return result.scalars().all()

    async def create(self, data: ProductCreate) -> ProductResponse:

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
