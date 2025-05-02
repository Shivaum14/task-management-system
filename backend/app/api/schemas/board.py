from pydantic import BaseModel


class BoardCreate(BaseModel):
    title: str


class BoardResponse(BaseModel):
    uid: str
    title: str
    owner: str
