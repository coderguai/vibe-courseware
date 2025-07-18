"""Modules API endpoints."""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from ...db.session import get_session
from ...models.module import Module, ModuleCreate, ModuleRead, ModuleUpdate
from ...services.course_service import CourseService
from ...services.module_service import ModuleService

router = APIRouter()
module_service = ModuleService()
course_service = CourseService()


@router.get("/", response_model=List[ModuleRead])
def read_modules(
    *,
    db: Session = Depends(get_session),
    course_id: int = Query(None),
    skip: int = 0,
    limit: int = 100,
    ordered: bool = Query(True),
) -> Any:
    """Get modules."""
    if course_id:
        if ordered:
            modules = module_service.get_by_course_id_ordered(
                db=db, course_id=course_id, skip=skip, limit=limit
            )
        else:
            modules = module_service.get_by_course_id(
                db=db, course_id=course_id, skip=skip, limit=limit
            )
    else:
        modules = module_service.get_multi(db=db, skip=skip, limit=limit)
    return modules


@router.post("/", response_model=ModuleRead)
def create_module(
    *,
    db: Session = Depends(get_session),
    module_in: ModuleCreate,
) -> Any:
    """Create module."""
    course = course_service.get(db=db, id=module_in.course_id)
    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )
    return module_service.create(db=db, obj_in=module_in)


@router.get("/{module_id}", response_model=ModuleRead)
def read_module(
    *,
    db: Session = Depends(get_session),
    module_id: int,
) -> Any:
    """Get module by ID."""
    module = module_service.get(db=db, id=module_id)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return module


@router.put("/{module_id}", response_model=ModuleRead)
def update_module(
    *,
    db: Session = Depends(get_session),
    module_id: int,
    module_in: ModuleUpdate,
) -> Any:
    """Update module."""
    module = module_service.get(db=db, id=module_id)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return module_service.update(db=db, db_obj=module, obj_in=module_in)


@router.delete("/{module_id}", response_model=ModuleRead)
def delete_module(
    *,
    db: Session = Depends(get_session),
    module_id: int,
) -> Any:
    """Delete module."""
    module = module_service.get(db=db, id=module_id)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return module_service.remove(db=db, id=module_id)