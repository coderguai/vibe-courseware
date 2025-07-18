"""Module service module."""

from typing import List

from sqlmodel import Session, select

from ..models.module import Module, ModuleCreate, ModuleUpdate
from .base_service import BaseService


class ModuleService(BaseService[Module, ModuleCreate, ModuleUpdate]):
    """Module service."""

    def __init__(self):
        """Initialize service."""
        super().__init__(Module)

    def get_by_course_id(self, db: Session, *, course_id: int, skip: int = 0, limit: int = 100) -> List[Module]:
        """Get modules by course id."""
        statement = select(Module).where(Module.course_id == course_id).offset(skip).limit(limit)
        return db.exec(statement).all()

    def get_by_course_id_ordered(self, db: Session, *, course_id: int, skip: int = 0, limit: int = 100) -> List[Module]:
        """Get modules by course id ordered by order field."""
        statement = (
            select(Module)
            .where(Module.course_id == course_id)
            .order_by(Module.order)
            .offset(skip)
            .limit(limit)
        )
        return db.exec(statement).all()