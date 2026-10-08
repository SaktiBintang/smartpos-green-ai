from decimal import Decimal
from typing import List
from uuid import UUID

from pydantic import BaseModel, Field


class TransactionItemCreate(BaseModel):
    product_id: UUID
    quantity: Decimal = Field(gt=0)
    discount_amount: Decimal = Field(default=Decimal("0"), ge=0)


class TransactionCreate(BaseModel):
    transaction_number: str = Field(min_length=1)
    payment_method: str = Field(min_length=1)
    customer_id: UUID | None = None
    discount_amount: Decimal = Field(default=Decimal("0"), ge=0)
    tax_amount: Decimal = Field(default=Decimal("0"), ge=0)
    items: List[TransactionItemCreate] = Field(min_length=1)
