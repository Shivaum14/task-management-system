from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, relationship

from app.core.db import Base
from app.core.orm import BaseMixin
from app.core.orm.utils import mapped_column
from app.core.utils import generate_uid

if TYPE_CHECKING:
    from app.models import Board


class Task(Base, BaseMixin):
    __tablename__ = "task"

    uid: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uid)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False, default="todo")  # todo, in_progress, done
    board_uid: Mapped[str] = mapped_column(
        String,
        ForeignKey("board.uid", ondelete="CASCADE"),
        nullable=False,
    )
    board: Mapped["Board"] = relationship("Board", back_populates="tasks")
