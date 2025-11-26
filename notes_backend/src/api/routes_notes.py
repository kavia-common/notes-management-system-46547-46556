from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.db import get_db
from src.crud.notes import (
    create_note as crud_create_note,
    delete_note as crud_delete_note,
    get_note as crud_get_note,
    list_notes as crud_list_notes,
    update_note as crud_update_note,
)
from src.schemas.note import NoteCreate, NoteOut, NoteUpdate

router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
)


# PUBLIC_INTERFACE
@router.get(
    "",
    response_model=List[NoteOut],
    summary="List notes",
    description="Retrieve a list of notes, optionally filtered by a search query across title and content.",
    responses={
        200: {"description": "List of notes returned successfully"},
    },
)
def list_notes_endpoint(
    q: Optional[str] = Query(default=None, description="Optional search text"),
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=100, ge=1, le=500, description="Max number of records to return"),
    db: Session = Depends(get_db),
) -> List[NoteOut]:
    """
    List notes with optional search.

    Parameters:
        q: Optional search string to match in title/content (case-insensitive).
        skip: Records to skip for pagination.
        limit: Max records to return.

    Returns:
        A list of notes sorted by creation date (newest first).
    """
    notes = crud_list_notes(db=db, q=q, skip=skip, limit=limit)
    return notes


# PUBLIC_INTERFACE
@router.post(
    "",
    response_model=NoteOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a note",
    description="Create and persist a new note.",
    responses={
        201: {"description": "Note created successfully"},
        422: {"description": "Validation error"},
    },
)
def create_note_endpoint(
    payload: NoteCreate,
    db: Session = Depends(get_db),
) -> NoteOut:
    """
    Create a note.

    Parameters:
        payload: NoteCreate schema containing title and optional content.

    Returns:
        The created note.
    """
    note = crud_create_note(db=db, data=payload)
    return note


# PUBLIC_INTERFACE
@router.get(
    "/{note_id}",
    response_model=NoteOut,
    summary="Get a note",
    description="Retrieve a single note by its ID.",
    responses={
        200: {"description": "Note retrieved successfully"},
        404: {"description": "Note not found"},
    },
)
def get_note_endpoint(
    note_id: int,
    db: Session = Depends(get_db),
) -> NoteOut:
    """
    Get a note by ID.

    Parameters:
        note_id: ID of the note.

    Returns:
        The requested note.

    Raises:
        HTTPException 404: If the note does not exist.
    """
    note = crud_get_note(db=db, note_id=note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


# PUBLIC_INTERFACE
@router.put(
    "/{note_id}",
    response_model=NoteOut,
    summary="Update a note",
    description="Update an existing note's fields by ID.",
    responses={
        200: {"description": "Note updated successfully"},
        404: {"description": "Note not found"},
        422: {"description": "Validation error"},
    },
)
def update_note_endpoint(
    note_id: int,
    payload: NoteUpdate,
    db: Session = Depends(get_db),
) -> NoteOut:
    """
    Update a note by ID.

    Parameters:
        note_id: ID of the note.
        payload: Fields to update.

    Returns:
        The updated note.

    Raises:
        HTTPException 404: If the note does not exist.
    """
    note = crud_update_note(db=db, note_id=note_id, data=payload)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


# PUBLIC_INTERFACE
@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a note",
    description="Delete a note by its ID.",
    responses={
        204: {"description": "Note deleted successfully"},
        404: {"description": "Note not found"},
    },
)
def delete_note_endpoint(
    note_id: int,
    db: Session = Depends(get_db),
) -> None:
    """
    Delete a note by ID.

    Parameters:
        note_id: ID of the note.

    Returns:
        No content on success.

    Raises:
        HTTPException 404: If the note does not exist.
    """
    deleted = crud_delete_note(db=db, note_id=note_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return None
