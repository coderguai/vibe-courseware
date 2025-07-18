"""Test API endpoints."""

from fastapi.testclient import TestClient
from sqlmodel import Session

from src.vibe_courseware.models.course import Course
from src.vibe_courseware.models.module import Module
from src.vibe_courseware.models.lesson import Lesson, LessonType


def test_create_course(client: TestClient) -> None:
    """Test create course endpoint."""
    response = client.post(
        "/api/v1/courses/",
        json={"title": "Test Course", "description": "Test Description"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Course"
    assert data["description"] == "Test Description"
    assert data["is_active"] is True
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_read_courses(client: TestClient, session: Session) -> None:
    """Test read courses endpoint."""
    # Create test courses
    course1 = Course(title="Course 1", description="Description 1")
    course2 = Course(title="Course 2", description="Description 2")
    session.add(course1)
    session.add(course2)
    session.commit()
    
    response = client.get("/api/v1/courses/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Course 1"
    assert data[1]["title"] == "Course 2"


def test_read_course(client: TestClient, session: Session) -> None:
    """Test read course endpoint."""
    # Create test course
    course = Course(title="Test Course", description="Test Description")
    session.add(course)
    session.commit()
    
    response = client.get(f"/api/v1/courses/{course.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Course"
    assert data["description"] == "Test Description"


def test_update_course(client: TestClient, session: Session) -> None:
    """Test update course endpoint."""
    # Create test course
    course = Course(title="Test Course", description="Test Description")
    session.add(course)
    session.commit()
    
    response = client.put(
        f"/api/v1/courses/{course.id}",
        json={"title": "Updated Course", "description": "Updated Description"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Course"
    assert data["description"] == "Updated Description"


def test_delete_course(client: TestClient, session: Session) -> None:
    """Test delete course endpoint."""
    # Create test course
    course = Course(title="Test Course", description="Test Description")
    session.add(course)
    session.commit()
    
    response = client.delete(f"/api/v1/courses/{course.id}")
    assert response.status_code == 200
    
    # Verify course is deleted
    response = client.get(f"/api/v1/courses/{course.id}")
    assert response.status_code == 404