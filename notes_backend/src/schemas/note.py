"""
Pydantic schemas for Notes.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class NoteBase(BaseModel):
    """Base attributes shared by create and update operations."""
    title: str = Field(..., description="The title of the note", min_length=1, max_length=255)
    content: Optional[str] = Field(None, description="The content/body of the note")


class NoteCreate(NoteBase):
    """Schema for creating a new note."""
    pass


class NoteUpdate(BaseModel):
    """Schema for updating an existing note. All fields optional to allow partial updates."""
    title: Optional[str] = Field(None, description="Updated title of the note", min_length=1, max_length=255)
    content: Optional[str] = Field(None, description="Updated content/body of the note")


class NoteOut(NoteBase):
    """Schema returned to clients when reading a note."""
    id: int = Field(..., description="Unique identifier for the note")
    created_at: datetime = Field(..., description="Timestamp when the note was created (UTC)")
    updated_at: datetime = Field(..., description="Timestamp when the note was last updated (UTC)")

    class Config:
        from_attributes = True  # pydantic v2 attribute to support ORM mode
