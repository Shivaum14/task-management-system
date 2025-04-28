from fastapi import APIRouter

from app.api.v1 import board, task

api_v1_router = APIRouter(prefix="/v1")

api_v1_router.include_router(board.router)
api_v1_router.include_router(task.router)
