import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Dict

from fastapi import FastAPI, Request

from app.config import get_settings
from app.api.v1 import api_v1_router

LOGGER = logging.getLogger("api")

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    LOGGER.info("Task Management Service API is Starting Up")
    yield
    LOGGER.info("Task Management Service API is Shutting Down")


app = FastAPI(
    title="Task Management API",
    description="API for the task management system",
    version=settings.VERSION,
    lifespan=lifespan,
)

app.include_router(api_v1_router)


@app.get("/health")
def health(request: Request) -> Dict[str, Any]:
    return {
        "status": "ok",
        "root_path": request.scope.get("root_path"),
        "host": request.headers.get("host"),
    }


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        workers=settings.WORKERS,
        log_level=settings.LOG_LEVEL,
        log_config=settings.LOG_CONFIG,
    )
