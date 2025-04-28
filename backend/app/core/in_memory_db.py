from typing import Dict
from uuid import UUID

from app.models.board import Board
from app.models.task import Task

boards: Dict[UUID, Board] = {}
tasks: Dict[UUID, Task] = {}
