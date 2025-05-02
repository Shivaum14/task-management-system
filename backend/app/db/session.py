from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

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

# Base class for declarative models (tables)
Base = declarative_base()


def get_db_session() -> Session:
    return SessionLocal()
