from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, declared_attr

from app.core.datetime import utc_now

from .utils import mapped_column


class TimestampMixin:
    @declared_attr.directive
    def created_at(cls) -> Mapped[datetime]:
        return mapped_column(DateTime, default=utc_now(), nullable=False, private=True)

    @declared_attr.directive
    def updated_at(cls) -> Mapped[datetime]:
        return mapped_column(DateTime, default=utc_now(), onupdate=utc_now(), nullable=False, private=True)


class AuditMixin(TimestampMixin):

    @declared_attr.directive
    def created_by(cls) -> Mapped[str]:
        return mapped_column(String, nullable=False, private=True)

    @declared_attr.directive
    def updated_by(cls) -> Mapped[str]:
        return mapped_column(String, nullable=False, private=True)
