"""
Database package initialization for the notes backend.

This package exposes commonly used database components, including:
- Base: Declarative base for SQLAlchemy models
- get_db: Dependency to retrieve a SQLAlchemy session for FastAPI routes
- engine: SQLAlchemy Engine instance configured for the application
"""

from .session import Base, engine, get_db

__all__ = ["Base", "engine", "get_db"]
