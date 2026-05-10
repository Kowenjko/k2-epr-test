from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    price: Decimal = Field(..., gt=0, decimal_places=2)
    sku: str | None = Field(None, max_length=100)


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    price: Decimal
    sku: str | None
    created_at: datetime
