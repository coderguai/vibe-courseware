"""Pagination utilities."""

from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel
from sqlmodel import Session, SQLModel, select

T = TypeVar("T", bound=SQLModel)


class Page(BaseModel, Generic[T]):
    """Page model for pagination."""

    items: List[T]
    total: int
    page: int
    size: int
    pages: int


def paginate(
    db: Session,
    model: type[T],
    *,
    page: int = 1,
    size: int = 10,
) -> Page[T]:
    """Paginate query results."""
    if page < 1:
        page = 1
    if size < 1:
        size = 10

    statement = select(model)
    total = db.exec(select(model)).all()
    total_count = len(total)

    statement = statement.offset((page - 1) * size).limit(size)
    items = db.exec(statement).all()

    pages = (total_count + size - 1) // size

    return Page(
        items=items,
        total=total_count,
        page=page,
        size=size,
        pages=pages,
    )