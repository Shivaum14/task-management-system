from typing import Any, Dict

import requests
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, SecurityScopes
from sqlalchemy.orm import Session

from app.config import get_settings
from app.core.db.session import get_db_session
from app.models.user import User
from app.services.user import get_or_create_user

from .jwt_validator import JWTValdiator

settings = get_settings()

oauth2_scheme = HTTPBearer(auto_error=True)
jwt_validator = JWTValdiator()


def fetch_user_info(token: str) -> Dict[str, Any]:
    """
    Fetches user information from the Auth0 userinfo endpoint.

    Args:
        token: The user's access token.

    Returns:
        A dictionary containing the user's information.

    Raises:
        HTTPException: If the request to the userinfo endpoint fails.
    """
    url = f"https://{settings.AUTH0_DOMAIN}/userinfo"
    headers = {"Authorization": f"Bearer {token}"}

    resp = requests.get(url, headers=headers)

    if resp.status_code != 200:
        raise HTTPException(status_code=401, detail="Failed to fetch user info")

    return resp.json()


def get_owner(
    security_scopes: SecurityScopes,
    crendentials: HTTPAuthorizationCredentials = Security(oauth2_scheme),
    session: Session = Depends(get_db_session),
) -> User:
    """
    Retrieves the requesting user based on the token provided.

    This function validates the token and fetches user information from the Auth0 userinfo endpoint.
    It then creates or retrieves the user from the database.

    This function is used as a dependency in FastAPI routes to ensure that the user is authenticated.

    Args:
        security_scopes: The scopes required by the endpoint.
        token: The user's access token.

    Returns:
        The user object associated with the access token.
    """
    token = crendentials.credentials
    payload = jwt_validator.validate_token(token, security_scopes.scopes)
    user_info = fetch_user_info(token)

    return get_or_create_user(
        session=session,
        sub=payload["sub"],
        email=user_info["email"],
        name=user_info["name"],
    )
