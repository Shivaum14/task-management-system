from uuid import UUID

from pydantic import BaseModel


class Board(BaseModel):
    uid: UUID
    title: str
    owner: str  # Will replace with real User ID later
