"""Course models module."""

from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

from .base import TimestampModel


class CourseBase(SQLModel):
    """Base course model."""

    title: str = Field(index=True)
    description: str
    is_active: bool = Field(default=True)


class Course(CourseBase, TimestampModel, table=True):
    """Course model."""

    __tablename__ = "courses"

    # Relationships
    modules: List["Module"] = Relationship(back_populates="course")


class CourseCreate(CourseBase):
    """Course create model."""

    pass


class CourseUpdate(SQLModel):
    """Course update model."""

    title: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class CourseRead(CourseBase):
    """Course read model."""

    id: int
    created_at: datetime
    updated_at: datetime


class CourseReadWithModules(CourseRead):
    """Course read model with modules."""

    from .module import ModuleRead

    modules: List[ModuleRead] = []