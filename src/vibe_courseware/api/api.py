"""API router module."""

from fastapi import APIRouter

from ..config import get_settings
from .endpoints import auth, courses, lessons, modules, users

settings = get_settings()

api_router = APIRouter(prefix=settings.API_V1_STR)

# Include routers from endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(courses.router, prefix="/courses", tags=["courses"])
api_router.include_router(modules.router, prefix="/modules", tags=["modules"])
api_router.include_router(lessons.router, prefix="/lessons", tags=["lessons"])