from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .enums import OrderStatus

from .schemas import OrderCreate, OrderResponse
from .repository import OrderRepository
from app.modules.product.repository import ProductRepository

from .models import Order, OrderItem
from app.modules.product.models import Product

from app.modules.client.services import ClientService


class OrderService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = OrderRepository(session)
        self.product_repository = ProductRepository(session)
        self.client_service = ClientService(session)

    async def get_order_by_id(self, order_id: int) -> OrderResponse:
        order = await self.repository.get_by_id(order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
            )

        return order

    async def create_order(self, data: OrderCreate) -> OrderResponse:
        await self.client_service.get_client(data.client_id)

        if not data.items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Order must contain at least one item",
            )

        product_ids = [item.product_id for item in data.items]

        products = await self.product_repository.get_multiple_by_ids(product_ids)

        products_map: dict[int, Product] = {product.id: product for product in products}

        missing_products = set(product_ids) - set(products_map.keys())

        if missing_products:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Products not found: {list(missing_products)}",
            )

        order = Order(
            client_id=data.client_id,
            notes=data.notes,
            status=OrderStatus.PENDING,
        )

        total = 0.0

        for item_data in data.items:
            product = products_map[item_data.product_id]

            unit_price = float(product.price)

            order_item = OrderItem(
                product_id=product.id,
                quantity=item_data.quantity,
                unit_price=unit_price,
            )

            order.items.append(order_item)

            total += unit_price * item_data.quantity

        order.total_amount = total

        self.session.add(order)

        await self.session.commit()
        await self.session.refresh(order)

        return await self.repository.get_by_id(order.id)

    async def get_order_by_client(self, client_id: int):
        await self.client_service.get_client(client_id)
        return await self.repository.get_by_client(client_id)
