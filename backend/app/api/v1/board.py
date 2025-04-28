from uuid import UUID, uuid4

from fastapi import APIRouter

from app.core.in_memory_db import boards, tasks
from app.models.board import Board
from app.schemas.board import BoardCreate, BoardResponse
from app.schemas.task import TaskResponse

router = APIRouter(prefix="/board", tags=["Board"])


@router.post("/", response_model=BoardResponse)
def create_board(board: BoardCreate) -> BoardResponse:
    board_uid = uuid4()
    new_board = Board(uid=board_uid, title=board.title, owner="anonymous")
    boards[board_uid] = new_board
    return BoardResponse(uid=str(board_uid), title=board.title, owner="anonymous")


@router.get("/", response_model=list[BoardResponse])
def list_boards() -> list[BoardResponse]:
    return [BoardResponse(uid=str(board.uid), title=board.title, owner=board.owner) for board in boards.values()]


@router.get("/{board_uid}/tasks", response_model=list[TaskResponse])
def list_tasks(board_uid: str) -> list[TaskResponse]:
    board_uuid = UUID(board_uid)
    return [
        TaskResponse(
            uid=str(task.uid),
            title=task.title,
            description=task.description,
            status=task.status,
            board_uid=str(task.board_uid),
        )
        for task in tasks.values()
        if task.board_uid == board_uuid
    ]
