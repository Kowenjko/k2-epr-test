from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class ClientCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr = Field(..., examples=["test@example.com"])
    phone: str | None = Field(None, max_length=50, examples=["+380971234567"])


class ClientResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    phone: str | None
    created_at: datetime
