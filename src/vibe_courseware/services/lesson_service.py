"""Lesson service module."""

from typing import List, Optional

from sqlmodel import Session, select

from ..models.lesson import Lesson, LessonCreate, LessonType, LessonUpdate
from .base_service import BaseService


class LessonService(BaseService[Lesson, LessonCreate, LessonUpdate]):
    """Lesson service."""

    def __init__(self):
        """Initialize service."""
        super().__init__(Lesson)

    def get_by_module_id(self, db: Session, *, module_id: int, skip: int = 0, limit: int = 100) -> List[Lesson]:
        """Get lessons by module id."""
        statement = select(Lesson).where(Lesson.module_id == module_id).offset(skip).limit(limit)
        return db.exec(statement).all()

    def get_by_module_id_ordered(self, db: Session, *, module_id: int, skip: int = 0, limit: int = 100) -> List[Lesson]:
        """Get lessons by module id ordered by order field."""
        statement = (
            select(Lesson)
            .where(Lesson.module_id == module_id)
            .order_by(Lesson.order)
            .offset(skip)
            .limit(limit)
        )
        return db.exec(statement).all()
        
    def get_by_type(self, db: Session, *, lesson_type: LessonType, skip: int = 0, limit: int = 100) -> List[Lesson]:
        """Get lessons by type."""
        statement = select(Lesson).where(Lesson.type == lesson_type).offset(skip).limit(limit)
        return db.exec(statement).all()