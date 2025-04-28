from uuid import UUID

from pydantic import BaseModel


class Task(BaseModel):
    uid: UUID
    title: str
    description: str
    status: str  # todo, in_progress, done
    board_uid: UUID
