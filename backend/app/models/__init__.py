"""Package initialization untuk app.models.

Memastikan seluruh model SQLAlchemy diimpor ke dalam namespace ini
sehingga secara otomatis terdaftar ke dalam Base.metadata untuk mendukung
autogenerate migrasi pada Alembic maupun penggunaan di aplikasi.
"""

from app.db.database import Base
from app.models.category import Category
from app.models.merchant import Merchant
from app.models.product import Product
from app.models.user import User

__all__ = [
    "Base",
    "Category",
    "Merchant",
    "Product",
    "User",
]
