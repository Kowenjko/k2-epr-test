from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, model_validator, ConfigDict

from .enums import OrderStatus

from app.modules.client.schemas import ClientResponse
from app.modules.product.schemas import ProductResponse


class OrderItemCreate(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0, le=10000, examples=[2])


class OrderCreate(BaseModel):
    client_id: int = Field(..., gt=0)
    notes: str | None = Field(None, max_length=1000)
    items: list[OrderItemCreate] = Field(..., min_length=1)

    @model_validator(mode="after")
    def validate_items_not_empty(self) -> "OrderCreate":
        if not self.items:
            raise ValueError("Order must contain at least one product")
        return self


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    subtotal: Decimal
    product: ProductResponse | None = None


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    client_id: int
    status: OrderStatus
    total_amount: Decimal
    notes: str | None
    created_at: datetime
    updated_at: datetime
    client: ClientResponse | None = None
    items: list[OrderItemResponse] = []


class OrderListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    client_id: int
    status: OrderStatus
    total_amount: Decimal
    notes: str | None
    created_at: datetime
    updated_at: datetime
    items_count: int = 0
