"""
core/database.py
────────────────
Database setup and session management using SQLModel.

SQLModel = SQLAlchemy (the query engine) + Pydantic (the validation).
You already know Pydantic. SQLModel just lets you query a DB with it.

Usage anywhere in the codebase:
    from core.database import get_session, create_db_tables
    with get_session() as session:
        session.add(job)
        session.commit()
"""

from sqlmodel import SQLModel, Session, create_engine
from contextlib import contextmanager
from config.settings import settings

# Create the engine once — this is the connection pool
engine = create_engine(
    settings.database_url,
    echo=False,  # set True to see SQL queries in console (useful for debugging)
    connect_args={"check_same_thread": False}  # needed for SQLite only
)


def create_db_tables():
    """
    Create all tables defined by SQLModel classes with table=True.
    Call this once at startup (main.py does this).
    Safe to call multiple times — won't recreate existing tables.
    """
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session():
    """
    Context manager for database sessions.

    Usage:
        with get_session() as session:
            jobs = session.exec(select(Job)).all()
    """
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
