"""Test models."""

import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from src.vibe_courseware.models.course import Course
from src.vibe_courseware.models.module import Module
from src.vibe_courseware.models.lesson import Lesson, LessonType


def test_course_model() -> None:
    """Test course model."""
    course = Course(title="Test Course", description="Test Description")
    assert course.title == "Test Course"
    assert course.description == "Test Description"
    assert course.is_active is True


def test_module_model() -> None:
    """Test module model."""
    module = Module(
        title="Test Module",
        description="Test Description",
        order=1,
        course_id=1,
    )
    assert module.title == "Test Module"
    assert module.description == "Test Description"
    assert module.order == 1
    assert module.course_id == 1


def test_lesson_model() -> None:
    """Test lesson model."""
    lesson = Lesson(
        title="Test Lesson",
        content="Test Content",
        type=LessonType.TEXT,
        order=1,
        module_id=1,
    )
    assert lesson.title == "Test Lesson"
    assert lesson.content == "Test Content"
    assert lesson.type == LessonType.TEXT
    assert lesson.order == 1
    assert lesson.module_id == 1


def test_relationships() -> None:
    """Test relationships between models."""
    # Create an in-memory SQLite database for testing
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        # Create a course
        course = Course(title="Test Course", description="Test Description")
        session.add(course)
        session.commit()
        
        # Create a module
        module = Module(
            title="Test Module",
            description="Test Description",
            order=1,
            course_id=course.id,
        )
        session.add(module)
        session.commit()
        
        # Create a lesson
        lesson = Lesson(
            title="Test Lesson",
            content="Test Content",
            type=LessonType.TEXT,
            order=1,
            module_id=module.id,
        )
        session.add(lesson)
        session.commit()
        
        # Test relationships
        session.refresh(course)
        session.refresh(module)
        session.refresh(lesson)
        
        assert len(course.modules) == 1
        assert course.modules[0].id == module.id
        assert module.course.id == course.id
        assert len(module.lessons) == 1
        assert module.lessons[0].id == lesson.id
        assert lesson.module.id == module.id