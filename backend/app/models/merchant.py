import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.category import Category
    from app.models.product import Product
    from app.models.user import User


class Merchant(Base):
    """Model SQLAlchemy untuk entitas Merchant pada sistem SmartPOS Green AI."""

    __tablename__ = "merchants"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Primary key UUID merchant",
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Nama merchant",
    )
    business_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Jenis usaha merchant",
    )
    phone: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="Nomor telepon merchant (opsional)",
    )
    address: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Alamat merchant (opsional)",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        default=lambda: datetime.now(timezone.utc),
        comment="Timestamp saat merchant dibuat",
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        default=lambda: datetime.now(timezone.utc),
        comment="Timestamp saat merchant diperbarui",
    )

    # Relationship ke User (dua arah)
    users: Mapped[List["User"]] = relationship(
        "User",
        back_populates="merchant",
        cascade="all, delete-orphan",
    )

    # Relationship ke Category (dua arah)
    categories: Mapped[List["Category"]] = relationship(
        "Category",
        back_populates="merchant",
        cascade="all, delete-orphan",
    )

    # Relationship ke Product (dua arah)
    products: Mapped[List["Product"]] = relationship(
        "Product",
        back_populates="merchant",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Merchant(id={self.id}, name={self.name!r}, business_type={self.business_type!r})>"
