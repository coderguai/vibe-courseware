"""Initialize database with sample data."""

import sys
from pathlib import Path

# Add the parent directory to the path so we can import the package
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlmodel import Session

from src.vibe_courseware.db.session import engine, init_db
from src.vibe_courseware.models.course import Course, CourseCreate
from src.vibe_courseware.models.module import Module, ModuleCreate
from src.vibe_courseware.models.lesson import Lesson, LessonCreate, LessonType
from src.vibe_courseware.models.user import User, UserRole
from src.vibe_courseware.utils.security import get_password_hash


def create_sample_data() -> None:
    """Create sample data."""
    init_db()
    
    with Session(engine) as session:
        # Check if we already have data
        course = session.query(Course).first()
        if course:
            print("Database already contains data. Skipping sample data creation.")
            return

        # Create admin user
        admin_user = User(
            email="admin@example.com",
            username="admin",
            full_name="Admin User",
            hashed_password=get_password_hash("admin123"),
            is_active=True,
            role=UserRole.ADMIN,
        )
        session.add(admin_user)
        
        # Create instructor user
        instructor_user = User(
            email="instructor@example.com",
            username="instructor",
            full_name="Instructor User",
            hashed_password=get_password_hash("instructor123"),
            is_active=True,
            role=UserRole.INSTRUCTOR,
        )
        session.add(instructor_user)
        
        # Create student user
        student_user = User(
            email="student@example.com",
            username="student",
            full_name="Student User",
            hashed_password=get_password_hash("student123"),
            is_active=True,
            role=UserRole.STUDENT,
        )
        session.add(student_user)
        
        # Create courses
        python_course = Course(
            title="Python Programming",
            description="Learn Python programming from scratch",
        )
        session.add(python_course)
        
        web_dev_course = Course(
            title="Web Development",
            description="Learn web development with HTML, CSS, and JavaScript",
        )
        session.add(web_dev_course)
        
        session.commit()
        
        # Create modules for Python course
        python_basics = Module(
            title="Python Basics",
            description="Learn the basics of Python programming",
            order=1,
            course_id=python_course.id,
        )
        session.add(python_basics)
        
        python_advanced = Module(
            title="Advanced Python",
            description="Learn advanced Python concepts",
            order=2,
            course_id=python_course.id,
        )
        session.add(python_advanced)
        
        # Create modules for Web Dev course
        html_css = Module(
            title="HTML & CSS",
            description="Learn the basics of HTML and CSS",
            order=1,
            course_id=web_dev_course.id,
        )
        session.add(html_css)
        
        javascript = Module(
            title="JavaScript",
            description="Learn JavaScript programming",
            order=2,
            course_id=web_dev_course.id,
        )
        session.add(javascript)
        
        session.commit()
        
        # Create lessons for Python Basics module
        intro_lesson = Lesson(
            title="Introduction to Python",
            content="Python is a high-level, interpreted programming language...",
            type=LessonType.TEXT,
            order=1,
            module_id=python_basics.id,
        )
        session.add(intro_lesson)
        
        variables_lesson = Lesson(
            title="Variables and Data Types",
            content="In Python, variables are created when you assign a value to them...",
            type=LessonType.TEXT,
            order=2,
            module_id=python_basics.id,
        )
        session.add(variables_lesson)
        
        quiz_lesson = Lesson(
            title="Python Basics Quiz",
            content="1. What is Python? 2. How do you create a variable in Python?...",
            type=LessonType.QUIZ,
            order=3,
            module_id=python_basics.id,
        )
        session.add(quiz_lesson)
        
        session.commit()
        
        print("Sample data created successfully!")


if __name__ == "__main__":
    create_sample_data()