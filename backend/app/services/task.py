from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import SessionDep
from app.api.schemas.task import TaskCreate
from app.models import Task
from app.services.board import board_exists


def create_task(session: SessionDep, task_in: TaskCreate) -> Task:
    if not board_exists(session, task_in.board_uid):
        raise ValueError("Board not found")

    db_task = Task(
        title=task_in.title,
        description=task_in.description,
        board_uid=task_in.board_uid,
        status="todo",
    )
    session.add(db_task)
    session.commit()
    return db_task


def get_tasks(session: Session, board_uid: Optional[str] = None) -> list[Task]:
    query = select(Task)
    if board_uid:
        query = query.where(Task.board_uid == board_uid)
    return session.execute(query).scalars().all()


def get_task_by_uid(session: Session, task_uid: str) -> Optional[Task]:
    query = select(Task).where(Task.uid == task_uid)
    return session.execute(query).scalar_one_or_none()


def update_task_status(session: Session, task_uid: str, status: str) -> Task:
    task = get_task_by_uid(session, task_uid)
    if not task:
        raise ValueError("Task not found")
    task.status = status
    session.commit()
    return task
