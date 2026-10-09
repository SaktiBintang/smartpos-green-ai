from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    category_id: UUID
    name: str = Field(min_length=1, max_length=255)
    sku: str = Field(min_length=1, max_length=100)
    price: Decimal = Field(ge=0, max_digits=14, decimal_places=2)
    cost_price: Decimal = Field(ge=0, max_digits=14, decimal_places=2)
    stock: Decimal = Field(
        default=Decimal("0"), ge=0, max_digits=14, decimal_places=3
    )
    unit: str = Field(min_length=1, max_length=50)


class ProductUpdate(BaseModel):
    category_id: UUID | None = None
    name: str | None = Field(default=None, min_length=1, max_length=255)
    sku: str | None = Field(default=None, min_length=1, max_length=100)
    price: Decimal | None = Field(
        default=None, ge=0, max_digits=14, decimal_places=2
    )
    cost_price: Decimal | None = Field(
        default=None, ge=0, max_digits=14, decimal_places=2
    )
    unit: str | None = Field(default=None, min_length=1, max_length=50)
    is_active: bool | None = None


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    merchant_id: UUID
    category_id: UUID
    name: str
    sku: str
    price: Decimal
    cost_price: Decimal
    stock: Decimal
    unit: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
