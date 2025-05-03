"""
Database engine and session setup for SQLAlchemy.

This module initializes the SQLAlchemy engine and session factory (`SessionLocal`)
using application settings. It also provides a `get_db_session` dependency for use
in FastAPI routes or services.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import get_settings

settings = get_settings()

engine = create_engine(
    str(settings.DB_URL),
    pool_size=20,  # number of connections to keep open
    max_overflow=10,  # allow 10 extra connections under heavy load
    pool_pre_ping=True,  # test connections is “alive” before using it
    pool_recycle=1800,  # refresh any connections older than 30 minutes
    echo=False,  # don’t log every SQL statement
)

SessionLocal = sessionmaker(
    autocommit=False,  # require you to call .commit() explicitly
    autoflush=False,  # don’t automatically push every change to the DB
    bind=engine,
)


def get_db_session() -> Session:
    """Creates a new database session."""
    return SessionLocal()
