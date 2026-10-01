import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.merchant import Merchant
    from app.models.product import Product


class Category(Base):
    """Model SQLAlchemy untuk entitas Category pada sistem SmartPOS Green AI."""

    __tablename__ = "categories"
    __table_args__ = (
        UniqueConstraint("merchant_id", "name", name="uq_categories_merchant_id_name"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Primary key UUID category",
    )
    merchant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("merchants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Foreign key ke merchants.id",
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Nama kategori produk",
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Deskripsi kategori produk (opsional)",
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default="true",
        nullable=False,
        comment="Status aktif kategori",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        default=lambda: datetime.now(timezone.utc),
        comment="Timestamp saat kategori dibuat",
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        default=lambda: datetime.now(timezone.utc),
        comment="Timestamp saat kategori diperbarui",
    )

    # Relationship ke Merchant (dua arah)
    merchant: Mapped["Merchant"] = relationship(
        "Merchant",
        back_populates="categories",
    )

    # Relationship ke Product (dua arah)
    products: Mapped[List["Product"]] = relationship(
        "Product",
        back_populates="category",
    )

    def __repr__(self) -> str:
        return f"<Category(id={self.id}, name={self.name!r}, merchant_id={self.merchant_id})>"
