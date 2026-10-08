import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import TYPE_CHECKING, List

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.category import Category
    from app.models.inventory_movement import InventoryMovement
    from app.models.merchant import Merchant
    from app.models.transaction_item import TransactionItem


class Product(Base):
    """Model SQLAlchemy untuk entitas Product pada sistem SmartPOS Green AI."""

    __tablename__ = "products"
    __table_args__ = (
        UniqueConstraint("merchant_id", "sku", name="uq_products_merchant_id_sku"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Primary key UUID product",
    )

    merchant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("merchants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Foreign key ke merchants.id",
    )

    category_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("categories.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
        comment="Foreign key ke categories.id",
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Nama produk",
    )

    sku: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Stock Keeping Unit produk",
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
        comment="Harga jual produk",
    )

    cost_price: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
        comment="Harga modal produk",
    )

    stock: Mapped[Decimal] = mapped_column(
        Numeric(14, 3),
        nullable=False,
        default=Decimal("0"),
        server_default="0",
        comment="Stok produk saat ini",
    )

    unit: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="Satuan produk, misalnya pcs, kg, liter",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default="true",
        nullable=False,
        comment="Status aktif produk",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        default=lambda: datetime.now(timezone.utc),
        comment="Timestamp saat produk dibuat",
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        default=lambda: datetime.now(timezone.utc),
        comment="Timestamp saat produk diperbarui",
    )

    # Relationship ke Merchant (dua arah)
    merchant: Mapped["Merchant"] = relationship(
        "Merchant",
        back_populates="products",
    )

    # Relationship ke Category (dua arah)
    category: Mapped["Category"] = relationship(
        "Category",
        back_populates="products",
    )

    # Relationship ke TransactionItem (satu produk dapat muncul di banyak item transaksi)
    transaction_items: Mapped[List["TransactionItem"]] = relationship(
        "TransactionItem",
        back_populates="product",
    )

    # Relationship ke InventoryMovement (dua arah)
    inventory_movements: Mapped[List["InventoryMovement"]] = relationship(
        "InventoryMovement",
        back_populates="product",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"<Product(id={self.id}, sku={self.sku!r}, "
            f"name={self.name!r}, merchant_id={self.merchant_id})>"
        )
