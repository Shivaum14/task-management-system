import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

LOGGER = logging.getLogger("api")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    LOGGER.info("Task Management Service API is Starting Up")
    yield
    LOGGER.info("Task Management Service API is Shutting Down")
