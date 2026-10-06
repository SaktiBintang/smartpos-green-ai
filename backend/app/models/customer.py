import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.merchant import Merchant
    from app.models.transaction import Transaction


class Customer(Base):
    """Model SQLAlchemy untuk entitas Customer pada sistem SmartPOS Green AI."""

    __tablename__ = "customers"
    __table_args__ = (
        UniqueConstraint(
            "merchant_id",
            "member_code",
            name="uq_customers_merchant_id_member_code",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Primary key UUID customer",
    )
    merchant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("merchants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Foreign key ke merchants.id",
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Nama customer",
    )
    phone: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="Nomor telepon customer",
    )
    email: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="Alamat email customer (opsional)",
    )
    member_code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Kode member customer",
    )
    address: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Alamat customer (opsional)",
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default="true",
        nullable=False,
        comment="Status aktif customer",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        default=lambda: datetime.now(timezone.utc),
        comment="Timestamp saat customer dibuat",
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        default=lambda: datetime.now(timezone.utc),
        comment="Timestamp saat customer diperbarui",
    )

    # Relationship ke Merchant (dua arah)
    merchant: Mapped["Merchant"] = relationship(
        "Merchant",
        back_populates="customers",
    )

    # Relationship ke Transaction (dua arah)
    transactions: Mapped[List["Transaction"]] = relationship(
        "Transaction",
        back_populates="customer",
    )

    def __repr__(self) -> str:
        return f"<Customer(id={self.id}, member_code={self.member_code!r}, name={self.name!r}, merchant_id={self.merchant_id})>"
