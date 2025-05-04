from fastapi import APIRouter

from . import board, task, user

api_v1_router = APIRouter(prefix="/v1")

api_v1_router.include_router(user.router)
api_v1_router.include_router(board.router)
api_v1_router.include_router(task.router)
