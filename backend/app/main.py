import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.middleware.error import ErrorMiddleware
from app.api.middleware.logging import LogMiddleware
from app.api.routers import api_v1_router, health_router
from app.config import get_settings
from app.core.lifespan import lifespan

LOGGER = logging.getLogger("api")

settings = get_settings()

app = FastAPI(
    title="Task Management API",
    description="API for the task management system",
    version=settings.VERSION,
    lifespan=lifespan,
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LogMiddleware)
app.add_middleware(ErrorMiddleware)

# Routers
app.include_router(api_v1_router)
app.include_router(health_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        workers=settings.WORKERS,
        log_level=settings.LOG_LEVEL,
        log_config=settings.LOG_CONFIG,
    )
