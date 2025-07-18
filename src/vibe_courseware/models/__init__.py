"""Models module."""

from .base import BaseModel, TimestampModel
from .course import Course, CourseCreate, CourseRead, CourseReadWithModules, CourseUpdate
from .lesson import Lesson, LessonCreate, LessonRead, LessonType, LessonUpdate
from .module import Module, ModuleCreate, ModuleRead, ModuleReadWithLessons, ModuleUpdate

__all__ = [
    "BaseModel",
    "TimestampModel",
    "Course",
    "CourseCreate",
    "CourseRead",
    "CourseReadWithModules",
    "CourseUpdate",
    "Module",
    "ModuleCreate",
    "ModuleRead",
    "ModuleReadWithLessons",
    "ModuleUpdate",
    "Lesson",
    "LessonCreate",
    "LessonRead",
    "LessonType",
    "LessonUpdate",
]