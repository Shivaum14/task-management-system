from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import Mapped, relationship

from app.core.orm import BaseMixin
from app.core.utils import generate_uid
from app.db.session import Base

if TYPE_CHECKING:
    from app.models import Board


class Task(Base, BaseMixin):
    __tablename__ = "task"

    uid: Mapped[str] = Column(String, primary_key=True, default=generate_uid)
    title: Mapped[str] = Column(String, nullable=False)
    description: Mapped[str] = Column(String, nullable=False)
    status: Mapped[str] = Column(String, nullable=False, default="todo")  # todo, in_progress, done
    board_uid: Mapped[str] = Column(
        String,
        ForeignKey("board.uid", ondelete="CASCADE"),
        nullable=False,
    )
    board: Mapped["Board"] = relationship("Board", back_populates="tasks")
