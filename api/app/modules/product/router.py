from typing import Annotated
from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from .schemas import ProductCreate, ProductResponse
from .services import ProductService

router = APIRouter(tags=["Products"])


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    session: Annotated[AsyncSession, Depends(get_db)],
):
    service = ProductService(session)
    return await service.create_product(product_data)


@router.get("/", response_model=list[ProductResponse])
async def get_products(
    session: Annotated[AsyncSession, Depends(get_db)],
):
    service = ProductService(session)
    return await service.all_products()


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    session: Annotated[AsyncSession, Depends(get_db)],
):
    service = ProductService(session)
    return await service.get_product(product_id)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    session: Annotated[AsyncSession, Depends(get_db)],
):
    service = ProductService(session)
    await service.delete_product(product_id)
