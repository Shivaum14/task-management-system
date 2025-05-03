from .serialization import SerializableMixin
from .audit import AuditMixin


class BaseMixin(SerializableMixin, AuditMixin):
    """Base mixin used to provide additional functionality for SQLAlchemy models."""

    pass
