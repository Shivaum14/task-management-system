from fastapi import APIRouter

from app.api.dependencies import SessionDep
from app.api.schemas.task import TaskCreate, TaskResponse, TaskUpdateStatus
from app.services.task import create_task as create_task_service
from app.services.task import update_task_status as update_task_status_service

router = APIRouter(prefix="/task", tags=["Task"])


@router.post("", response_model=TaskResponse)
def create_task(session: SessionDep, task_input: TaskCreate) -> TaskResponse:
    task = create_task_service(session, task_input)
    return task.to_schema(TaskResponse)


@router.patch("/{task_uid}/status", response_model=TaskResponse)
def update_task_status(session: SessionDep, task_uid: str, status_update: TaskUpdateStatus) -> TaskResponse:
    task = update_task_status_service(session, task_uid, status_update.status)
    return task.to_schema(TaskResponse)
