"""
CRUD operations for the Note model.
"""

from typing import Optional, Sequence

from sqlalchemy.orm import Session
from sqlalchemy import select, or_

from src.db import models
from src.schemas.note import NoteCreate, NoteUpdate


# PUBLIC_INTERFACE
def get_note(db: Session, note_id: int) -> Optional[models.Note]:
    """Retrieve a single note by its ID.

    Args:
        db: SQLAlchemy Session.
        note_id: The ID of the note to fetch.

    Returns:
        The Note instance if found, otherwise None.
    """
    return db.get(models.Note, note_id)


# PUBLIC_INTERFACE
def list_notes(db: Session, q: Optional[str] = None, skip: int = 0, limit: int = 100) -> Sequence[models.Note]:
    """List notes with optional search query.

    Args:
        db: SQLAlchemy Session.
        q: Optional search string to filter by title or content (case-insensitive).
        skip: Number of records to skip (pagination).
        limit: Maximum number of records to return.

    Returns:
        A sequence of Note instances.
    """
    stmt = select(models.Note).order_by(models.Note.created_at.desc())

    if q:
        like = f"%{q}%"
        stmt = stmt.where(
            or_(models.Note.title.ilike(like), models.Note.content.ilike(like))
        )

    stmt = stmt.offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()


# PUBLIC_INTERFACE
def create_note(db: Session, data: NoteCreate) -> models.Note:
    """Create and persist a new note.

    Args:
        db: SQLAlchemy Session.
        data: NoteCreate payload.

    Returns:
        The created Note instance.
    """
    note = models.Note(title=data.title, content=data.content)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


# PUBLIC_INTERFACE
def update_note(db: Session, note_id: int, data: NoteUpdate) -> Optional[models.Note]:
    """Update an existing note with provided fields.

    Args:
        db: SQLAlchemy Session.
        note_id: ID of the note to update.
        data: NoteUpdate payload (partial fields allowed).

    Returns:
        The updated Note instance if found, else None.
    """
    note = db.get(models.Note, note_id)
    if not note:
        return None

    payload = data.model_dump(exclude_unset=True)
    for k, v in payload.items():
        setattr(note, k, v)

    db.add(note)
    db.commit()
    db.refresh(note)
    return note


# PUBLIC_INTERFACE
def delete_note(db: Session, note_id: int) -> bool:
    """Delete a note by ID.

    Args:
        db: SQLAlchemy Session.
        note_id: The ID of the note to delete.

    Returns:
        True if a note was deleted, False if note not found.
    """
    note = db.get(models.Note, note_id)
    if not note:
        return False
    db.delete(note)
    db.commit()
    return True
