"""JWT service implementation."""

from datetime import datetime, timedelta, timezone
from typing import Mapping, Optional
from uuid import UUID

from jose import JWTError, jwt
from {{cookiecutter.project_slug}}.common.core.config.settings import settings


class JWTService:
    """Service for handling JWT operations."""

    def create_access_token(self, data: Mapping[str, str]) -> str:
        """Create a new access token."""
        expires_delta = timedelta(minutes=settings.jwt_access_token_expire_minutes)
        expire = datetime.now(timezone.utc) + expires_delta

        to_encode = dict(data)
        to_encode["exp"] = str(int(expire.timestamp()))

        encoded_jwt = jwt.encode(
            to_encode,
            settings.jwt_secret_key,
            algorithm=settings.jwt_algorithm,
        )

        return encoded_jwt

    def decode_token(self, token: str) -> Optional[UUID]:
        """Decode and validate a JWT token."""
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret_key,
                algorithms=[settings.jwt_algorithm],
            )
            user_id = payload.get("sub")
            if user_id is None:
                return None
            return UUID(user_id)
        except (JWTError, ValueError):
            return None
