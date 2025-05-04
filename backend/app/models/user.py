from sqlalchemy import String
from sqlalchemy.orm import Mapped

from app.core.db import Base
from app.core.orm import BaseMixin
from app.core.orm.utils import mapped_column


class User(Base, BaseMixin):
    __tablename__ = "user"

    email: Mapped[str] = mapped_column(String, primary_key=True, nullable=False)
    auth0_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String)
