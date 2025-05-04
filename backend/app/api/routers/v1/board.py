from fastapi import APIRouter, HTTPException

from app.api.schemas.board import BoardCreate, BoardResponse
from app.api.schemas.task import TaskResponse
from app.core.context import Context
from app.services.board import create_board as create_board_db
from app.services.board import get_board_by_uid, get_boards

router = APIRouter(prefix="/board", tags=["Board"])


@router.post("", response_model=BoardResponse)
def create_board(context: Context, board_input: BoardCreate) -> BoardResponse:
    new_board = create_board_db(context.session, context.owner, board_input)
    return new_board.to_schema(BoardResponse)


@router.get("", response_model=list[BoardResponse])
def list_boards(context: Context) -> list[BoardResponse]:
    boards = get_boards(context.session)
    return [board.to_schema(BoardResponse) for board in boards]


@router.get("/{board_uid}/tasks", response_model=list[TaskResponse])
def list_tasks(context: Context, board_uid: str) -> list[TaskResponse]:
    board = get_board_by_uid(context.session, board_uid)

    if not board:
        raise HTTPException(status_code=404, detail="Board not found.")

    tasks = board.tasks
    return [task.to_schema(TaskResponse) for task in tasks]
