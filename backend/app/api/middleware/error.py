import logging
from typing import Awaitable, Callable

from fastapi import HTTPException, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class ErrorMiddleware(BaseHTTPMiddleware):
    LOGGER = logging.getLogger("exception-middleware")

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        try:
            response = await call_next(request)
            return response
        except HTTPException as e:
            # Forward intentional HTTP Exceptions
            self.LOGGER.info(f"HTTP Exception: {str(e)}, Path: {request.url.path}")
            raise e
        except Exception as e:
            self.LOGGER.exception(f"Unhandled Exception: {str(e)}, Path: {request.url.path}")
            return JSONResponse(
                content={"error": f"Unexpected error: {request.state.request_id}"},
                status_code=500,
            )
