import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Numeric, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.product import Product
    from app.models.transaction import Transaction


class TransactionItem(Base):
    """Model SQLAlchemy untuk detail item pada sebuah transaksi."""

    __tablename__ = "transaction_items"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Primary key UUID transaction item",
    )

    transaction_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("transactions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Foreign key ke transactions.id",
    )

    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
        comment="Foreign key ke products.id",
    )

    quantity: Mapped[Decimal] = mapped_column(
        Numeric(14, 3),
        nullable=False,
        default=Decimal("0"),
        server_default="0",
        comment="Jumlah produk yang dibeli",
    )

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
        default=Decimal("0"),
        server_default="0",
        comment="Harga produk saat transaksi",
    )

    discount_amount: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
        default=Decimal("0"),
        server_default="0",
        comment="Jumlah diskon untuk item",
    )

    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
        default=Decimal("0"),
        server_default="0",
        comment="Subtotal item setelah diskon",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        default=lambda: datetime.now(timezone.utc),
        comment="Timestamp saat item transaksi dibuat",
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        default=lambda: datetime.now(timezone.utc),
        comment="Timestamp saat item transaksi diperbarui",
    )

    transaction: Mapped["Transaction"] = relationship(
        "Transaction",
        back_populates="items",
    )

    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="transaction_items",
    )

    def __repr__(self) -> str:
        return (
            f"<TransactionItem(id={self.id}, "
            f"transaction_id={self.transaction_id}, "
            f"product_id={self.product_id}, "
            f"quantity={self.quantity}, "
            f"subtotal={self.subtotal})>"
        )