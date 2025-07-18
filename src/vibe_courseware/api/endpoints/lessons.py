"""Lessons API endpoints."""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from ...db.session import get_session
from ...models.lesson import Lesson, LessonCreate, LessonRead, LessonType, LessonUpdate
from ...services.lesson_service import LessonService
from ...services.module_service import ModuleService

router = APIRouter()
lesson_service = LessonService()
module_service = ModuleService()


@router.get("/", response_model=List[LessonRead])
def read_lessons(
    *,
    db: Session = Depends(get_session),
    module_id: int = Query(None),
    lesson_type: LessonType = Query(None),
    skip: int = 0,
    limit: int = 100,
    ordered: bool = Query(True),
) -> Any:
    """Get lessons."""
    if module_id:
        if ordered:
            lessons = lesson_service.get_by_module_id_ordered(
                db=db, module_id=module_id, skip=skip, limit=limit
            )
        else:
            lessons = lesson_service.get_by_module_id(
                db=db, module_id=module_id, skip=skip, limit=limit
            )
    elif lesson_type:
        lessons = lesson_service.get_by_type(
            db=db, lesson_type=lesson_type, skip=skip, limit=limit
        )
    else:
        lessons = lesson_service.get_multi(db=db, skip=skip, limit=limit)
    return lessons


@router.post("/", response_model=LessonRead)
def create_lesson(
    *,
    db: Session = Depends(get_session),
    lesson_in: LessonCreate,
) -> Any:
    """Create lesson."""
    module = module_service.get(db=db, id=lesson_in.module_id)
    if not module:
        raise HTTPException(
            status_code=404,
            detail="Module not found",
        )
    return lesson_service.create(db=db, obj_in=lesson_in)


@router.get("/{lesson_id}", response_model=LessonRead)
def read_lesson(
    *,
    db: Session = Depends(get_session),
    lesson_id: int,
) -> Any:
    """Get lesson by ID."""
    lesson = lesson_service.get(db=db, id=lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


@router.put("/{lesson_id}", response_model=LessonRead)
def update_lesson(
    *,
    db: Session = Depends(get_session),
    lesson_id: int,
    lesson_in: LessonUpdate,
) -> Any:
    """Update lesson."""
    lesson = lesson_service.get(db=db, id=lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson_service.update(db=db, db_obj=lesson, obj_in=lesson_in)


@router.delete("/{lesson_id}", response_model=LessonRead)
def delete_lesson(
    *,
    db: Session = Depends(get_session),
    lesson_id: int,
) -> Any:
    """Delete lesson."""
    lesson = lesson_service.get(db=db, id=lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson_service.remove(db=db, id=lesson_id)