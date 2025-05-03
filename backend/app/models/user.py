from sqlalchemy import String
from sqlalchemy.orm import Mapped

from app.core.db import Base
from app.core.orm import BaseMixin
from app.core.orm.utils import mapped_column
from app.core.utils import generate_uid


class User(Base, BaseMixin):
    __tablename__ = "user"

    uid: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uid)
    auth0_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String)
