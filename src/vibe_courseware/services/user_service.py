"""User service module."""

from typing import Optional

from sqlmodel import Session, select

from ..models.user import User, UserCreate, UserUpdate
from ..utils.security import get_password_hash, verify_password
from .base_service import BaseService


class UserService(BaseService[User, UserCreate, UserUpdate]):
    """User service."""

    def __init__(self):
        """Initialize service."""
        super().__init__(User)

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """Create user."""
        db_obj = User(
            email=obj_in.email,
            username=obj_in.username,
            full_name=obj_in.full_name,
            hashed_password=get_password_hash(obj_in.password),
            is_active=obj_in.is_active,
            role=obj_in.role,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: UserUpdate
    ) -> User:
        """Update user."""
        update_data = obj_in.model_dump(exclude_unset=True)
        if "password" in update_data and update_data["password"]:
            update_data["hashed_password"] = get_password_hash(update_data["password"])
            del update_data["password"]
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        """Authenticate user."""
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """Get user by email."""
        statement = select(User).where(User.email == email)
        return db.exec(statement).first()

    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        """Get user by username."""
        statement = select(User).where(User.username == username)
        return db.exec(statement).first()

    def is_active(self, user: User) -> bool:
        """Check if user is active."""
        return user.is_active

    def is_admin(self, user: User) -> bool:
        """Check if user is admin."""
        return user.role == "admin"

    def is_instructor(self, user: User) -> bool:
        """Check if user is instructor."""
        return user.role == "instructor"