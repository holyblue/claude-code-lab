"""
Database connection and session management.

This module provides database connection setup and session management
using SQLAlchemy ORM.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

# Create SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
    echo=settings.DEBUG,
)

# Create SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for declarative models
Base = declarative_base()


def get_db():
    """
    Dependency function to get database session.

    Yields:
        Session: SQLAlchemy database session

    Example:
        ```python
        from fastapi import Depends
        from app.database import get_db

        @app.get("/items")
        def read_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
        ```
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database by creating all tables.

    This function should be called when the application starts.
    It will create all tables defined in SQLAlchemy models.

    Example:
        ```python
        from app.database import init_db

        # In main.py
        init_db()
        ```
    """
    # Import all models here to ensure they are registered with Base
    # This will be done after models are created
    from app import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
