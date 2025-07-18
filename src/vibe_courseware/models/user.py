"""User models module."""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import EmailStr, Field
from sqlmodel import SQLModel

from .base import TimestampModel


class UserRole(str, Enum):
    """User role enum."""

    ADMIN = "admin"
    INSTRUCTOR = "instructor"
    STUDENT = "student"


class UserBase(SQLModel):
    """Base user model."""

    email: EmailStr = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.STUDENT


class User(UserBase, TimestampModel, table=True):
    """User model."""

    __tablename__ = "users"

    hashed_password: str


class UserCreate(UserBase):
    """User create model."""

    password: str


class UserUpdate(SQLModel):
    """User update model."""

    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[UserRole] = None


class UserRead(UserBase):
    """User read model."""

    id: int
    created_at: datetime
    updated_at: datetime


class Token(SQLModel):
    """Token model."""

    access_token: str
    token_type: str


class TokenPayload(SQLModel):
    """Token payload model."""

    sub: Optional[int] = None