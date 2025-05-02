from typing import TYPE_CHECKING

from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, relationship

from app.core.orm import BaseMixin
from app.core.utils import generate_uid
from app.db.session import Base

if TYPE_CHECKING:
    from app.models import Task


class Board(Base, BaseMixin):
    __tablename__ = "board"

    uid: Mapped[str] = Column(String, primary_key=True, default=generate_uid)
    title: Mapped[str] = Column(String, nullable=False)
    owner: Mapped[str] = Column(String, nullable=False)

    tasks: Mapped[list["Task"]] = relationship(
        "Task", back_populates="board", cascade="all, delete", passive_deletes=True
    )
