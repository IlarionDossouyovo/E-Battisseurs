"""Database configuration for E-Battisseurs"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database URL from environment
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///ebattisseurs.db")

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    echo=False
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    """Get database session"""
    return SessionLocal()

def get_db():
    """Get database session (for FastAPI dependency)"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables"""
    from backend.models import Base
    Base.metadata.create_all(bind=engine)
    return engine