"""Declarative base class for SQLAlchemy ORM models."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.

    This class provides the declarative foundation used by all models in the application.
    Inherit from this class to create a new model that will be tracked by SQLAlchemy's ORM.

    It is required by SQLAlchemy to define metadata and mapping configuration for all models.
    """

    pass
