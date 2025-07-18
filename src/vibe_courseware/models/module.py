"""Module models module."""

from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

from .base import TimestampModel


class ModuleBase(SQLModel):
    """Base module model."""

    title: str = Field(index=True)
    description: str
    order: int = Field(default=0)
    course_id: int = Field(foreign_key="courses.id")


class Module(ModuleBase, TimestampModel, table=True):
    """Module model."""

    __tablename__ = "modules"

    # Relationships
    course: "Course" = Relationship(back_populates="modules")
    lessons: List["Lesson"] = Relationship(back_populates="module")


class ModuleCreate(ModuleBase):
    """Module create model."""

    pass


class ModuleUpdate(SQLModel):
    """Module update model."""

    title: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None


class ModuleRead(ModuleBase):
    """Module read model."""

    id: int
    created_at: datetime
    updated_at: datetime


class ModuleReadWithLessons(ModuleRead):
    """Module read model with lessons."""

    from .lesson import LessonRead

    lessons: List[LessonRead] = []