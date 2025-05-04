from typing import Annotated

from fastapi import Depends, Security
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from app.core.auth import get_owner
from app.core.db import get_db_session
from app.models.user import User


class RequestContext(BaseModel):
    """Request context model."""

    owner: User
    session: Session

    model_config = ConfigDict(arbitrary_types_allowed=True)


def get_context(owner: User = Security(get_owner), session: Session = Depends(get_db_session)) -> RequestContext:
    """Dependency function to provide the request context."""

    return RequestContext(owner=owner, session=session)


Context = Annotated[RequestContext, Security(get_context)]
