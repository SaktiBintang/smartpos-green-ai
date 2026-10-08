from decimal import Decimal
from typing import Any, Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.inventory_movement import InventoryMovement
from app.models.product import Product
from app.models.transaction import Transaction
from app.models.transaction_item import TransactionItem


class TransactionService:
    """Business logic inti untuk transaksi SmartPOS Green AI."""

    @staticmethod
    def calculate_item_subtotal(
        quantity: Decimal,
        unit_price: Decimal,
        discount_amount: Decimal = Decimal("0"),
    ) -> Decimal:
        """Menghitung subtotal satu item setelah diskon."""
        if quantity <= Decimal("0"):
            raise ValueError("Quantity harus lebih besar dari 0.")

        if unit_price < Decimal("0"):
            raise ValueError("Unit price tidak boleh negatif.")

        if discount_amount < Decimal("0"):
            raise ValueError("Discount amount tidak boleh negatif.")

        gross_amount = quantity * unit_price

        if discount_amount > gross_amount:
            raise ValueError(
                "Discount item tidak boleh melebihi nilai item."
            )

        return gross_amount - discount_amount

    @staticmethod
    def calculate_transaction_subtotal(
        item_subtotals: Iterable[Decimal],
    ) -> Decimal:
        """Menghitung subtotal transaksi dari seluruh subtotal item."""
        subtotal = sum(item_subtotals, Decimal("0"))

        if subtotal < Decimal("0"):
            raise ValueError("Subtotal transaksi tidak boleh negatif.")

        return subtotal

    @staticmethod
    def calculate_total(
        subtotal: Decimal,
        discount_amount: Decimal = Decimal("0"),
        tax_amount: Decimal = Decimal("0"),
    ) -> Decimal:
        """Menghitung total akhir transaksi."""
        if subtotal < Decimal("0"):
            raise ValueError("Subtotal tidak boleh negatif.")

        if discount_amount < Decimal("0"):
            raise ValueError(
                "Discount transaksi tidak boleh negatif."
            )

        if tax_amount < Decimal("0"):
            raise ValueError("Tax tidak boleh negatif.")

        if discount_amount > subtotal:
            raise ValueError(
                "Discount transaksi tidak boleh melebihi subtotal."
            )

        total = subtotal - discount_amount + tax_amount

        if total < Decimal("0"):
            raise ValueError("Total transaksi tidak boleh negatif.")

        return total

    @staticmethod
    def create_transaction(
        db: Session,
        merchant_id,
        transaction_number: str,
        payment_method: str,
        items: Iterable[dict[str, Any]],
        customer_id=None,
        discount_amount: Decimal = Decimal("0"),
        tax_amount: Decimal = Decimal("0"),
    ) -> Transaction:
        """
        Membuat transaksi penjualan secara atomic.

        Harga produk selalu diambil dari database, bukan dari client.
        Perubahan stok dan inventory movement berada dalam satu
        database transaction.
        """
        items = list(items)

        if not items:
            raise ValueError("Transaksi harus memiliki minimal satu item.")

        if not transaction_number.strip():
            raise ValueError("Transaction number wajib diisi.")

        if not payment_method.strip():
            raise ValueError("Payment method wajib diisi.")

        if discount_amount < Decimal("0"):
            raise ValueError(
                "Discount transaksi tidak boleh negatif."
            )

        if tax_amount < Decimal("0"):
            raise ValueError("Tax tidak boleh negatif.")

        product_ids = [item["product_id"] for item in items]

        if len(product_ids) != len(set(product_ids)):
            raise ValueError(
                "Produk yang sama tidak boleh muncul lebih dari sekali "
                "dalam satu transaksi."
            )

        try:
            # Nested transaction aman digunakan ketika Session sudah
            # memiliki transaction aktif akibat query sebelumnya.
            with db.begin_nested():
                if customer_id is not None:
                    customer = db.scalar(
                        select(Customer).where(
                            Customer.id == customer_id,
                            Customer.merchant_id == merchant_id,
                            Customer.is_active.is_(True),
                        )
                    )

                    if customer is None:
                        raise ValueError(
                            "Customer tidak ditemukan atau bukan milik merchant."
                        )

                transaction = Transaction(
                    merchant_id=merchant_id,
                    customer_id=customer_id,
                    transaction_number=transaction_number,
                    payment_method=payment_method,
                    payment_status="paid",
                    status="completed",
                    discount_amount=discount_amount,
                    tax_amount=tax_amount,
                )

                db.add(transaction)
                db.flush()

                item_subtotals: list[Decimal] = []

                for item in items:
                    product_id = item["product_id"]
                    quantity = Decimal(str(item["quantity"]))
                    item_discount = Decimal(
                        str(item.get("discount_amount", "0"))
                    )

                    # Lock row product untuk mencegah race condition
                    # ketika dua transaksi mengakses stok yang sama.
                    product = db.scalar(
                        select(Product)
                        .where(
                            Product.id == product_id,
                            Product.merchant_id == merchant_id,
                            Product.is_active.is_(True),
                        )
                        .with_for_update()
                    )

                    if product is None:
                        raise ValueError(
                            f"Produk {product_id} tidak ditemukan "
                            "atau bukan milik merchant."
                        )

                    if quantity <= Decimal("0"):
                        raise ValueError(
                            f"Quantity produk '{product.name}' "
                            "harus lebih besar dari 0."
                        )

                    if item_discount < Decimal("0"):
                        raise ValueError(
                            f"Discount produk '{product.name}' "
                            "tidak boleh negatif."
                        )

                    stock_before = product.stock

                    if quantity > stock_before:
                        raise ValueError(
                            f"Stok produk '{product.name}' tidak mencukupi. "
                            f"Stok tersedia: {stock_before}."
                        )

                    # Harga selalu berasal dari database.
                    unit_price = product.price

                    item_subtotal = (
                        TransactionService.calculate_item_subtotal(
                            quantity=quantity,
                            unit_price=unit_price,
                            discount_amount=item_discount,
                        )
                    )

                    stock_after = stock_before - quantity

                    transaction_item = TransactionItem(
                        transaction_id=transaction.id,
                        product_id=product.id,
                        quantity=quantity,
                        unit_price=unit_price,
                        discount_amount=item_discount,
                        subtotal=item_subtotal,
                    )

                    db.add(transaction_item)

                    # Kurangi stok.
                    product.stock = stock_after

                    # Catat perubahan stok.
                    inventory_movement = InventoryMovement(
                        merchant_id=merchant_id,
                        product_id=product.id,
                        movement_type="sale",
                        quantity=-quantity,
                        stock_before=stock_before,
                        stock_after=stock_after,
                        reference_type="transaction",
                        reference_id=transaction.id,
                        notes=(
                            f"Penjualan melalui transaksi "
                            f"{transaction.transaction_number}"
                        ),
                    )

                    db.add(inventory_movement)

                    item_subtotals.append(item_subtotal)

                subtotal = (
                    TransactionService.calculate_transaction_subtotal(
                        item_subtotals
                    )
                )

                total = TransactionService.calculate_total(
                    subtotal=subtotal,
                    discount_amount=discount_amount,
                    tax_amount=tax_amount,
                )

                transaction.subtotal = subtotal
                transaction.total_amount = total

                db.flush()

            # Commit seluruh transaction.
            db.commit()

            return transaction

        except Exception:
            db.rollback()
            raise
