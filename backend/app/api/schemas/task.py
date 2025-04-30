from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: str
    board_uid: str


class TaskUpdateStatus(BaseModel):
    status: str  # todo, in_progress, done


class TaskResponse(BaseModel):
    uid: str
    title: str
    description: str
    status: str
    board_uid: str
