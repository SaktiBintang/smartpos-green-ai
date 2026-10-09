from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:
    @staticmethod
    def create_category(
        db: Session,
        merchant_id: UUID,
        payload: CategoryCreate,
    ) -> Category:
        try:
            with db.begin_nested():
                name = payload.name.strip()
                if not name:
                    raise ValueError("Nama kategori tidak boleh kosong.")

                duplicate = db.scalar(
                    select(Category.id).where(
                        Category.merchant_id == merchant_id,
                        Category.name == name,
                    )
                )
                if duplicate is not None:
                    raise ValueError("Nama kategori sudah digunakan merchant ini.")

                category = Category(
                    merchant_id=merchant_id,
                    name=name,
                    description=(
                        payload.description.strip()
                        if payload.description is not None
                        else None
                    ),
                )
                db.add(category)
                db.flush()

            db.commit()
            db.refresh(category)
            return category

        except IntegrityError as exc:
            db.rollback()
            raise ValueError(
                "Kategori gagal disimpan. Periksa nama kategori."
            ) from exc
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def list_categories(
        db: Session,
        merchant_id: UUID,
        include_inactive: bool = False,
    ) -> list[Category]:
        statement = select(Category).where(
            Category.merchant_id == merchant_id
        )
        if not include_inactive:
            statement = statement.where(Category.is_active.is_(True))

        statement = statement.order_by(Category.created_at.desc())
        return list(db.scalars(statement).all())

    @staticmethod
    def get_category(
        db: Session,
        merchant_id: UUID,
        category_id: UUID,
    ) -> Category:
        category = db.scalar(
            select(Category).where(
                Category.id == category_id,
                Category.merchant_id == merchant_id,
            )
        )
        if category is None:
            raise ValueError("Kategori tidak ditemukan.")
        return category

    @staticmethod
    def update_category(
        db: Session,
        merchant_id: UUID,
        category_id: UUID,
        payload: CategoryUpdate,
    ) -> Category:
        try:
            with db.begin_nested():
                category = db.scalar(
                    select(Category)
                    .where(
                        Category.id == category_id,
                        Category.merchant_id == merchant_id,
                    )
                    .with_for_update()
                )
                if category is None:
                    raise ValueError("Kategori tidak ditemukan.")

                changes = payload.model_dump(exclude_unset=True)
                if not changes:
                    raise ValueError("Tidak ada perubahan yang dikirim.")

                if "name" in changes:
                    name = changes["name"].strip()
                    if not name:
                        raise ValueError("Nama kategori tidak boleh kosong.")

                    duplicate = db.scalar(
                        select(Category.id).where(
                            Category.merchant_id == merchant_id,
                            Category.name == name,
                            Category.id != category.id,
                        )
                    )
                    if duplicate is not None:
                        raise ValueError(
                            "Nama kategori sudah digunakan merchant ini."
                        )
                    changes["name"] = name

                if "description" in changes:
                    description = changes["description"]
                    changes["description"] = (
                        description.strip() if description is not None else None
                    )

                for field, value in changes.items():
                    setattr(category, field, value)

                db.flush()

            db.commit()
            db.refresh(category)
            return category

        except IntegrityError as exc:
            db.rollback()
            raise ValueError(
                "Kategori gagal diperbarui. Periksa nama kategori."
            ) from exc
        except Exception:
            db.rollback()
            raise
