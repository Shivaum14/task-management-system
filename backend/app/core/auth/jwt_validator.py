from typing import Any, Dict

import requests  # noqa: F401
from fastapi import HTTPException, status
from jose import JWTError, jwt

from app.config import get_settings

settings = get_settings()


class JWTValidator:
    def __init__(self) -> None:
        jwks_url = f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json"
        self.jwks = self.get_jwk(jwks_url)

    def get_jwk(self, jwks_url: str) -> list[Dict[str, Any]]:
        resp = requests.get(jwks_url)
        return resp.json()["keys"]

    def validate_token(self, token: str, required_scopes: list[str]) -> Dict[str, Any]:
        try:
            header = jwt.get_unverified_header(token)
            rsa_key = next((key for key in self.jwks if key["kid"] == header["kid"]), None)
            if not rsa_key:
                raise HTTPException(status_code=401, detail="Invalid Token")

            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=["RS256"],
                audience=settings.AUTH0_API_AUDIENCE,
                issuer=f"https://{settings.AUTH0_DOMAIN}/",
            )
            self.validate_scopes(payload, required_scopes)
            return payload
        except JWTError:
            raise HTTPException(status_code=401, detail="Token validation failed")

    def validate_scopes(self, payload: Dict[str, Any], required_scopes: list[str]) -> None:
        token_scopes = payload.get("scope", "")
        assert isinstance(token_scopes, str), "Token scopes should be a string"

        token_scope_set = set(token_scopes.split())
        required_scopes_set = set(required_scopes)

        if not required_scopes_set.issubset(token_scope_set):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
