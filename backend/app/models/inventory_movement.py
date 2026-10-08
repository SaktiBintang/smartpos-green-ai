import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.merchant import Merchant
    from app.models.product import Product


class InventoryMovement(Base):
    """Model SQLAlchemy untuk mencatat setiap perubahan stok produk."""

    __tablename__ = "inventory_movements"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Primary key UUID inventory movement",
    )

    merchant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("merchants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Foreign key ke merchants.id",
    )

    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
        comment="Foreign key ke products.id",
    )

    movement_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="Jenis pergerakan stok",
    )

    quantity: Mapped[Decimal] = mapped_column(
        Numeric(14, 3),
        nullable=False,
        default=Decimal("0"),
        server_default="0",
        comment="Jumlah perubahan stok",
    )

    stock_before: Mapped[Decimal] = mapped_column(
        Numeric(14, 3),
        nullable=False,
        default=Decimal("0"),
        server_default="0",
        comment="Stok sebelum perubahan",
    )

    stock_after: Mapped[Decimal] = mapped_column(
        Numeric(14, 3),
        nullable=False,
        default=Decimal("0"),
        server_default="0",
        comment="Stok setelah perubahan",
    )

    reference_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="Jenis sumber perubahan stok",
    )

    reference_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
        comment="ID sumber perubahan stok tanpa foreign key",
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Catatan perubahan stok",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        default=lambda: datetime.now(timezone.utc),
        comment="Timestamp saat inventory movement dibuat",
    )

    merchant: Mapped["Merchant"] = relationship(
        "Merchant",
        back_populates="inventory_movements",
    )

    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="inventory_movements",
    )

    def __repr__(self) -> str:
        return (
            f"<InventoryMovement(id={self.id}, "
            f"product_id={self.product_id}, "
            f"movement_type={self.movement_type}, "
            f"quantity={self.quantity}, "
            f"stock_before={self.stock_before}, "
            f"stock_after={self.stock_after})>"
        )
