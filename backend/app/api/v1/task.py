from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException

from app.core.in_memory_db import boards, tasks
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdateStatus

router = APIRouter(prefix="/task", tags=["Task"])


@router.post("/", response_model=TaskResponse)
def create_task(task: TaskCreate) -> TaskResponse:
    if UUID(task.board_uid) not in boards:
        raise HTTPException(status_code=404, detail="Board not found.")

    task_uid = uuid4()
    new_task = Task(
        uid=task_uid,
        title=task.title,
        description=task.description,
        status="todo",
        board_uid=UUID(task.board_uid),
    )
    tasks[task_uid] = new_task
    return TaskResponse(
        uid=str(task_uid),
        title=task.title,
        description=task.description,
        status="todo",
        board_uid=task.board_uid,
    )


@router.patch("/{task_uid}/status", response_model=TaskResponse)
def update_task_status(task_uid: str, status_update: TaskUpdateStatus) -> TaskResponse:
    task_uuid = UUID(task_uid)
    if task_uuid not in tasks:
        raise HTTPException(status_code=404, detail="Task not found.")

    task = tasks[task_uuid]
    task.status = status_update.status
    tasks[task_uuid] = task
    return TaskResponse(
        uid=str(task.uid),
        title=task.title,
        description=task.description,
        status=task.status,
        board_uid=str(task.board_uid),
    )
