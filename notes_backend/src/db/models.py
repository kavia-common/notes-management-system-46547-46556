"""
SQLAlchemy models for the notes backend.
"""

from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Text
from .session import Base


class Note(Base):
    """
    ORM model representing a Note entity.
    """
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    content = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        index=True,
    )

    def __repr__(self) -> str:
        return f"<Note id={self.id} title={self.title!r}>"
