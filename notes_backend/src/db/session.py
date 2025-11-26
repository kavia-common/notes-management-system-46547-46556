"""
Session and engine setup for SQLAlchemy.

- Uses DATABASE_URL env var if present; otherwise defaults to sqlite:///./data/notes.db
- Ensures the ./data directory exists for SQLite file persistence
- Exposes `engine`, `SessionLocal`, `Base`, and FastAPI dependency `get_db`
"""

import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Determine database URL from environment or default to local SQLite file
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/notes.db")

# Ensure ./data directory exists for SQLite file
if DATABASE_URL.startswith("sqlite:///./"):
    data_dir = os.path.dirname(DATABASE_URL.replace("sqlite:///", ""))
    if data_dir and not os.path.exists(data_dir):
        os.makedirs(data_dir, exist_ok=True)

# Create SQLAlchemy engine
engine_kwargs = {}
# For SQLite, need check_same_thread=False for multithreaded FastAPI usage
if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, **engine_kwargs)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base
Base = declarative_base()


# PUBLIC_INTERFACE
def get_db() -> Generator:
    """Provide a database session for request lifetime.

    Yields:
        sqlalchemy.orm.Session: A SQLAlchemy session bound to the configured engine.
    Ensures the session is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
