import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, sessionmaker

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# Konfigurasi koneksi PostgreSQL dari environment variable (tanpa hardcode password)
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "smartpos_green_ai")

# Gunakan DATABASE_URL jika didefinisikan secara langsung di environment,
# atau susun URL koneksi SQLAlchemy 2.x dengan driver psycopg 3 (postgresql+psycopg)
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    DATABASE_URL = URL.create(
        drivername="postgresql+psycopg",
        username=DB_USER,
        password=DB_PASSWORD if DB_PASSWORD else None,
        host=DB_HOST,
        port=int(DB_PORT) if DB_PORT else 5432,
        database=DB_NAME,
    )

# Engine SQLAlchemy untuk aplikasi FastAPI
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

# Factory sesi database untuk FastAPI
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# Base class deklaratif untuk model SQLAlchemy (SQLAlchemy 2.x DeclarativeBase)
class Base(DeclarativeBase):
    pass


# Dependency FastAPI untuk mendapatkan session database per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
