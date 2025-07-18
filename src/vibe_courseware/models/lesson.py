"""Lesson models module."""

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from .base import TimestampModel


class LessonType(str, Enum):
    """Lesson type enum."""

    VIDEO = "video"
    TEXT = "text"
    QUIZ = "quiz"
    ASSIGNMENT = "assignment"


class LessonBase(SQLModel):
    """Base lesson model."""

    title: str = Field(index=True)
    content: str
    type: LessonType = Field(default=LessonType.TEXT)
    order: int = Field(default=0)
    module_id: int = Field(foreign_key="modules.id")


class Lesson(LessonBase, TimestampModel, table=True):
    """Lesson model."""

    __tablename__ = "lessons"

    # Relationships
    module: "Module" = Relationship(back_populates="lessons")


class LessonCreate(LessonBase):
    """Lesson create model."""

    pass


class LessonUpdate(SQLModel):
    """Lesson update model."""

    title: Optional[str] = None
    content: Optional[str] = None
    type: Optional[LessonType] = None
    order: Optional[int] = None


class LessonRead(LessonBase):
    """Lesson read model."""

    id: int
    created_at: datetime
    updated_at: datetime