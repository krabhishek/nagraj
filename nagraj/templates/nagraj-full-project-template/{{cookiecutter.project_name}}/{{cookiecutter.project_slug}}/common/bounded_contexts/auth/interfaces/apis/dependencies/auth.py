"""Authentication dependencies."""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from {{cookiecutter.project_slug}}.common.bounded_contexts.auth.application.dtos.user_dto import (
    UserDTO,
)
from {{cookiecutter.project_slug}}.common.bounded_contexts.auth.application.handlers.command_handlers import (
    UserCommandHandlers,
)
from {{cookiecutter.project_slug}}.common.bounded_contexts.auth.application.services.auth_service import (
    AuthService,
)
from {{cookiecutter.project_slug}}.common.bounded_contexts.auth.domain.events.user_events import (
    PasswordChangedEvent,
    UserAuthenticatedEvent,
    UserCreatedEvent,
)
from {{cookiecutter.project_slug}}.common.bounded_contexts.auth.infrastructure.event_handlers.auth_event_handler import (
    AuthEventHandler,
)
from {{cookiecutter.project_slug}}.common.bounded_contexts.auth.infrastructure.repositories.user_repository import (
    UserRepository,
)
from {{cookiecutter.project_slug}}.common.core.events.event_dispatcher import EventDispatcher

from ..security.jwt import JWTService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


def get_auth_service() -> AuthService:
    """Get the auth service instance."""
    repository = UserRepository()
    event_dispatcher = EventDispatcher()

    # Create and register event handler
    event_handler = AuthEventHandler()
    event_dispatcher.register(UserCreatedEvent, event_handler.handle)
    event_dispatcher.register(UserAuthenticatedEvent, event_handler.handle)
    event_dispatcher.register(PasswordChangedEvent, event_handler.handle)

    handlers = UserCommandHandlers(repository, event_dispatcher)

    return AuthService(
        create_user_handler=handlers,
        authenticate_user_handler=handlers,
        change_password_handler=handlers,
        query_handler=handlers,
    )


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> UserDTO:
    """Get current authenticated user from JWT token."""
    user_id = JWTService().decode_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await auth_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
