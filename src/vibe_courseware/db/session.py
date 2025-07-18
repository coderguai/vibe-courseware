"""Database session module."""

from typing import Generator

from sqlmodel import Session, SQLModel, create_engine

from ..config import get_settings

settings = get_settings()

engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {},
)


def get_session() -> Generator[Session, None, None]:
    """Get database session."""
    with Session(engine) as session:
        yield session


def init_db() -> None:
    """Initialize database."""
    SQLModel.metadata.create_all(engine)