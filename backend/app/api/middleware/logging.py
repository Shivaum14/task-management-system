import logging
import time
from typing import Awaitable, Callable
from urllib.parse import urlparse
from uuid import uuid4

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logger import MergeLoggerAdapter


class LogMiddleware(BaseHTTPMiddleware):
    LOGGER = logging.getLogger("http")

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        request_id = str(uuid4())

        log = MergeLoggerAdapter(self.LOGGER, extra={"request_id": request_id})
        request.state.log = log
        request.state.request_id = request_id

        extra = {
            "request_id": request_id,
            "method": request.method,
            "url": str(request.url),
            "path": urlparse(str(request.url)).path,
            "remote": {
                "host": request.client.host if request.client else "",
                "port": request.client.port if request.client else "",
            },
            "headers": dict(request.headers.items()),
            "query": dict(request.query_params.items()),
        }

        log.info(
            "request",
            extra=extra,
        )

        before = time.time()
        response = await call_next(request)
        duration = time.time() - before

        log.info(
            "response",
            extra={
                **extra,
                "status_code": response.status_code,
                "media_type": response.media_type,
                "headers": dict(response.headers.items()),
                "duration_ms": round(duration * 1000, 2),
            },
        )

        return response
