"""
Database connection — MySQL via SQLAlchemy + PyMySQL
Reads credentials from .env file
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "password")
DB_NAME = os.getenv("DB_NAME", "disaster_db")

# quote_plus encodes special chars like @ # $ % in passwords
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{quote_plus(DB_PASS)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    DATABASE_URL,
    echo=False,               # Set True to log SQL queries during dev
    pool_pre_ping=True,       # Reconnect if MySQL drops idle connections
    pool_recycle=3600,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency for FastAPI endpoints — yields a DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
