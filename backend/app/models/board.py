from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, relationship

from app.core.orm import BaseMixin
from app.core.orm.utils import mapped_column
from app.core.utils import generate_uid
from app.db.base import Base

if TYPE_CHECKING:
    from app.models import Task


class Board(Base, BaseMixin):
    __tablename__ = "board"

    uid: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uid)
    title: Mapped[str] = mapped_column(String, nullable=False)
    owner: Mapped[str] = mapped_column(String, nullable=False)

    tasks: Mapped[list["Task"]] = relationship(
        "Task", back_populates="board", cascade="all, delete", passive_deletes=True
    )
