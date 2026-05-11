from typing import Annotated
from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from .schemas import OrderCreate, OrderResponse
from .services import OrderService

router = APIRouter(tags=["Orders"])


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreate,
    session: AsyncSession = Depends(get_db),
):
    service = OrderService(session)
    return await service.create_order(order_data)


@router.get(
    "/client/{client_id}",
    response_model=list[OrderResponse],
    status_code=status.HTTP_200_OK,
)
async def get_order_by_client(
    client_id: int,
    session: Annotated[AsyncSession, Depends(get_db)],
):
    service = OrderService(session)
    return await service.get_order_by_client(client_id)


@router.get("/{order_id}", response_model=OrderResponse, status_code=status.HTTP_200_OK)
async def get_order(
    order_id: int,
    session: Annotated[AsyncSession, Depends(get_db)],
):
    service = OrderService(session)
    return await service.get_order_by_id(order_id)
