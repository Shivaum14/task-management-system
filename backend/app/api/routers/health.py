from typing import Any, Dict

from fastapi import APIRouter, Request

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
def health(request: Request) -> Dict[str, Any]:
    return {
        "status": "ok",
        "root_path": request.scope.get("root_path"),
        "host": request.headers.get("host"),
    }
