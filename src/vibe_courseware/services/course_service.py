"""Course service module."""

from typing import List, Optional

from sqlmodel import Session, select

from ..models.course import Course, CourseCreate, CourseUpdate
from .base_service import BaseService


class CourseService(BaseService[Course, CourseCreate, CourseUpdate]):
    """Course service."""

    def __init__(self):
        """Initialize service."""
        super().__init__(Course)

    def get_by_title(self, db: Session, *, title: str) -> Optional[Course]:
        """Get course by title."""
        statement = select(Course).where(Course.title == title)
        return db.exec(statement).first()

    def get_active_courses(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Course]:
        """Get active courses."""
        statement = select(Course).where(Course.is_active == True).offset(skip).limit(limit)  # noqa: E712
        return db.exec(statement).all()