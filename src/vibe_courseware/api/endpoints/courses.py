"""Courses API endpoints."""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from ...db.session import get_session
from ...models.course import Course, CourseCreate, CourseRead, CourseUpdate
from ...services.course_service import CourseService

router = APIRouter()
course_service = CourseService()


@router.get("/", response_model=List[CourseRead])
def read_courses(
    *,
    db: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
    active_only: bool = Query(False),
) -> Any:
    """Get courses."""
    if active_only:
        courses = course_service.get_active_courses(db=db, skip=skip, limit=limit)
    else:
        courses = course_service.get_multi(db=db, skip=skip, limit=limit)
    return courses


@router.post("/", response_model=CourseRead)
def create_course(
    *,
    db: Session = Depends(get_session),
    course_in: CourseCreate,
) -> Any:
    """Create course."""
    course = course_service.get_by_title(db=db, title=course_in.title)
    if course:
        raise HTTPException(
            status_code=400,
            detail="Course with this title already exists.",
        )
    return course_service.create(db=db, obj_in=course_in)


@router.get("/{course_id}", response_model=CourseRead)
def read_course(
    *,
    db: Session = Depends(get_session),
    course_id: int,
) -> Any:
    """Get course by ID."""
    course = course_service.get(db=db, id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.put("/{course_id}", response_model=CourseRead)
def update_course(
    *,
    db: Session = Depends(get_session),
    course_id: int,
    course_in: CourseUpdate,
) -> Any:
    """Update course."""
    course = course_service.get(db=db, id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course_service.update(db=db, db_obj=course, obj_in=course_in)


@router.delete("/{course_id}", response_model=CourseRead)
def delete_course(
    *,
    db: Session = Depends(get_session),
    course_id: int,
) -> Any:
    """Delete course."""
    course = course_service.get(db=db, id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course_service.remove(db=db, id=course_id)