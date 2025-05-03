from .audit import AuditMixin
from .serialization import SerializableMixin


class BaseMixin(SerializableMixin, AuditMixin):
    """Base mixin used to provide additional functionality for SQLAlchemy models."""

    pass
