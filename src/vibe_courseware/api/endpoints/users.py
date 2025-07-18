"""Users API endpoints."""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from ...db.session import get_session
from ...models.user import User, UserCreate, UserRead, UserUpdate
from ...services.user_service import UserService
from ..deps import get_current_active_user, get_current_admin_user

router = APIRouter()
user_service = UserService()


@router.get("/", response_model=List[UserRead])
def read_users(
    *,
    db: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin_user),
) -> Any:
    """Get users."""
    users = user_service.get_multi(db=db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=UserRead)
def create_user(
    *,
    db: Session = Depends(get_session),
    user_in: UserCreate,
    current_user: User = Depends(get_current_admin_user),
) -> Any:
    """Create user."""
    user = user_service.get_by_email(db=db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with this email already exists.",
        )
    user = user_service.get_by_username(db=db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with this username already exists.",
        )
    return user_service.create(db=db, obj_in=user_in)


@router.get("/me", response_model=UserRead)
def read_user_me(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Get current user."""
    return current_user


@router.put("/me", response_model=UserRead)
def update_user_me(
    *,
    db: Session = Depends(get_session),
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Update current user."""
    return user_service.update(db=db, db_obj=current_user, obj_in=user_in)


@router.get("/{user_id}", response_model=UserRead)
def read_user(
    *,
    db: Session = Depends(get_session),
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
) -> Any:
    """Get user by ID."""
    user = user_service.get(db=db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserRead)
def update_user(
    *,
    db: Session = Depends(get_session),
    user_id: int,
    user_in: UserUpdate,
    current_user: User = Depends(get_current_admin_user),
) -> Any:
    """Update user."""
    user = user_service.get(db=db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user_service.update(db=db, db_obj=user, obj_in=user_in)


@router.delete("/{user_id}", response_model=UserRead)
def delete_user(
    *,
    db: Session = Depends(get_session),
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
) -> Any:
    """Delete user."""
    user = user_service.get(db=db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user_service.remove(db=db, id=user_id)