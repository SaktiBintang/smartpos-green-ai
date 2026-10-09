from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.inventory_movement import InventoryMovement
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:
    @staticmethod
    def create_product(
        db: Session,
        merchant_id: UUID,
        payload: ProductCreate,
    ) -> Product:
        try:
            with db.begin_nested():
                category = db.scalar(
                    select(Category).where(
                        Category.id == payload.category_id,
                        Category.merchant_id == merchant_id,
                        Category.is_active.is_(True),
                    )
                )
                if category is None:
                    raise ValueError(
                        "Kategori tidak ditemukan, tidak aktif, "
                        "atau bukan milik merchant ini."
                    )

                duplicate = db.scalar(
                    select(Product.id).where(
                        Product.merchant_id == merchant_id,
                        Product.sku == payload.sku,
                    )
                )
                if duplicate is not None:
                    raise ValueError("SKU sudah digunakan merchant ini.")

                product = Product(
                    merchant_id=merchant_id,
                    category_id=payload.category_id,
                    name=payload.name.strip(),
                    sku=payload.sku.strip(),
                    price=payload.price,
                    cost_price=payload.cost_price,
                    stock=payload.stock,
                    unit=payload.unit.strip(),
                )
                db.add(product)
                db.flush()

                if product.stock > 0:
                    db.add(
                        InventoryMovement(
                            merchant_id=merchant_id,
                            product_id=product.id,
                            movement_type="opening_stock",
                            quantity=product.stock,
                            stock_before=Decimal("0"),
                            stock_after=product.stock,
                            reference_type="product",
                            reference_id=product.id,
                            notes="Stok awal saat produk dibuat",
                        )
                    )
                    db.flush()

            db.commit()
            db.refresh(product)
            return product

        except IntegrityError as exc:
            db.rollback()
            raise ValueError(
                "Produk gagal disimpan. Pastikan SKU belum digunakan."
            ) from exc
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def list_products(
        db: Session,
        merchant_id: UUID,
        include_inactive: bool = False,
    ) -> list[Product]:
        statement = select(Product).where(
            Product.merchant_id == merchant_id
        )
        if not include_inactive:
            statement = statement.where(Product.is_active.is_(True))

        statement = statement.order_by(Product.created_at.desc())
        return list(db.scalars(statement).all())

    @staticmethod
    def get_product(
        db: Session,
        merchant_id: UUID,
        product_id: UUID,
    ) -> Product:
        product = db.scalar(
            select(Product).where(
                Product.id == product_id,
                Product.merchant_id == merchant_id,
            )
        )
        if product is None:
            raise ValueError("Produk tidak ditemukan.")
        return product

    @staticmethod
    def update_product(
        db: Session,
        merchant_id: UUID,
        product_id: UUID,
        payload: ProductUpdate,
    ) -> Product:
        try:
            with db.begin_nested():
                product = db.scalar(
                    select(Product)
                    .where(
                        Product.id == product_id,
                        Product.merchant_id == merchant_id,
                    )
                    .with_for_update()
                )
                if product is None:
                    raise ValueError("Produk tidak ditemukan.")

                changes = payload.model_dump(exclude_unset=True)
                if not changes:
                    raise ValueError("Tidak ada perubahan yang dikirim.")

                if "stock" in changes:
                    raise ValueError(
                        "Stok tidak boleh diubah melalui update produk. "
                        "Gunakan pencatatan pergerakan inventori."
                    )

                if "category_id" in changes:
                    category_id = changes["category_id"]
                    if category_id is None:
                        raise ValueError("Kategori tidak boleh kosong.")

                    category = db.scalar(
                        select(Category).where(
                            Category.id == category_id,
                            Category.merchant_id == merchant_id,
                            Category.is_active.is_(True),
                        )
                    )
                    if category is None:
                        raise ValueError(
                            "Kategori tidak ditemukan, tidak aktif, "
                            "atau bukan milik merchant ini."
                        )

                if "name" in changes:
                    changes["name"] = changes["name"].strip()
                if "sku" in changes:
                    changes["sku"] = changes["sku"].strip()
                if "unit" in changes:
                    changes["unit"] = changes["unit"].strip()

                if "sku" in changes:
                    duplicate = db.scalar(
                        select(Product.id).where(
                            Product.merchant_id == merchant_id,
                            Product.sku == changes["sku"],
                            Product.id != product.id,
                        )
                    )
                    if duplicate is not None:
                        raise ValueError("SKU sudah digunakan merchant ini.")

                for field, value in changes.items():
                    setattr(product, field, value)

                db.flush()

            db.commit()
            db.refresh(product)
            return product

        except IntegrityError as exc:
            db.rollback()
            raise ValueError(
                "Produk gagal diperbarui. Periksa SKU dan kategori."
            ) from exc
        except Exception:
            db.rollback()
            raise
