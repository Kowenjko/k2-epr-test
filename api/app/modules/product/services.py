from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import ProductCreate, ProductResponse

from .repository import ProductRepository


class ProductService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = ProductRepository(session)

    async def create_product(self, product_data: ProductCreate) -> ProductResponse:
        existing_product = await self.repository.get_by_sku(product_data.sku)
        if existing_product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product with this SKU already exists",
            )
        new_product = await self.repository.create(product_data)
        await self.session.commit()
        return new_product

    async def get_product(self, product_id: int) -> ProductResponse:
        product = await self.repository.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )
        return product

    async def all_products(self) -> list[ProductResponse]:
        return await self.repository.all()

    async def delete_product(self, product_id: int) -> None:
        product = await self.get_product(product_id)

        await self.repository.delete(product)
        await self.session.commit()
