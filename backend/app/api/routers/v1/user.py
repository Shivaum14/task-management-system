from typing import Any, Dict

from fastapi import APIRouter

from app.core.context import Context

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/profile")
def get_profile(context: Context) -> Dict[str, Any]:
    owner = context.owner
    return {"email": owner.email, "name": owner.name}
