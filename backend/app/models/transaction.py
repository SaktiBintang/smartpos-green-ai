import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.customer import Customer
    from app.models.merchant import Merchant
    from app.models.transaction_item import TransactionItem


class Transaction(Base):
    """Model SQLAlchemy untuk entitas Transaction pada sistem SmartPOS Green AI."""

    __tablename__ = "transactions"
    __table_args__ = (
        UniqueConstraint(
            "merchant_id",
            "transaction_number",
            name="uq_transactions_merchant_id_transaction_number",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Primary key UUID transaction",
    )
    merchant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("merchants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Foreign key ke merchants.id",
    )
    customer_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customers.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="Foreign key ke customers.id (opsional)",
    )
    transaction_number: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Nomor transaksi",
    )
    transaction_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        default=lambda: datetime.now(timezone.utc),
        comment="Tanggal dan waktu transaksi",
    )
    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
        default=Decimal("0"),
        server_default="0",
        comment="Subtotal transaksi sebelum diskon dan pajak",
    )
    discount_amount: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
        default=Decimal("0"),
        server_default="0",
        comment="Jumlah diskon transaksi",
    )
    tax_amount: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
        default=Decimal("0"),
        server_default="0",
        comment="Jumlah pajak transaksi",
    )
    total_amount: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
        default=Decimal("0"),
        server_default="0",
        comment="Total akhir transaksi",
    )
    payment_method: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="Metode pembayaran",
    )
    payment_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="pending",
        server_default="pending",
        comment="Status pembayaran",
    )
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="draft",
        server_default="draft",
        comment="Status transaksi",
    )
    notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Catatan transaksi (opsional)",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        default=lambda: datetime.now(timezone.utc),
        comment="Timestamp saat transaksi dibuat",
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        default=lambda: datetime.now(timezone.utc),
        comment="Timestamp saat transaksi diperbarui",
    )

    # Relationship ke Merchant (dua arah)
    merchant: Mapped["Merchant"] = relationship(
        "Merchant",
        back_populates="transactions",
    )

    # Relationship ke Customer (dua arah)
    customer: Mapped[Optional["Customer"]] = relationship(
        "Customer",
        back_populates="transactions",
    )

    # Relationship ke TransactionItem (satu transaksi memiliki banyak item)
    items: Mapped[List["TransactionItem"]] = relationship(
        "TransactionItem",
        back_populates="transaction",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"<Transaction(id={self.id}, "
            f"transaction_number={self.transaction_number!r}, "
            f"merchant_id={self.merchant_id}, "
            f"total_amount={self.total_amount})>"
        )