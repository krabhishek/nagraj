from typing import Optional
from uuid import UUID

from pydantic import EmailStr

from {{cookiecutter.project_slug}}.common.core.logging import LoggerService

from ..commands.authenticate_user import (
    AuthenticateUserCommand,
    AuthenticateUserHandler,
)
from ..commands.change_password import ChangePasswordCommand, ChangePasswordHandler
from ..commands.create_user import CreateUserCommand, CreateUserHandler
from ..dtos.user_dto import UserDTO
from ..queries.get_user import GetUserByEmailQuery, GetUserByIdQuery, UserQueryHandler


class AuthService:
    """Authentication service implementation."""

    def __init__(
        self,
        create_user_handler: CreateUserHandler,
        authenticate_user_handler: AuthenticateUserHandler,
        change_password_handler: ChangePasswordHandler,
        query_handler: UserQueryHandler,
    ) -> None:
        """Initialize the service with required handlers."""
        self._create_user_handler = create_user_handler
        self._authenticate_user_handler = authenticate_user_handler
        self._change_password_handler = change_password_handler
        self._query_handler = query_handler
        self._logger = LoggerService().get_logger({"module": "auth_service"})

    async def register_user(self, email: str, password: str) -> UserDTO:
        """Register a new user."""
        try:
            # Check if user exists
            existing_user = await self._query_handler.get_by_email(
                GetUserByEmailQuery(email=email)
            )
            if existing_user:
                raise ValueError("User with this email already exists")

            # Create user
            command = CreateUserCommand(email=email, password=password)
            user = await self._create_user_handler.handle(command)
            self._logger.info(f"User registered successfully: {email}")
            return UserDTO.from_aggregate(user)
        except ValueError as e:
            self._logger.error(f"Registration failed for {email}: {str(e)}")
            raise
        except Exception as e:
            self._logger.error(
                f"Unexpected error during registration for {email}: {str(e)}"
            )
            raise ValueError("Failed to register user") from e

    async def authenticate_user(self, email: str, password: str) -> UserDTO:
        """Authenticate a user."""
        try:
            command = AuthenticateUserCommand(email=email, password=password)
            user = await self._authenticate_user_handler.handle(command)
            self._logger.info(f"User authenticated successfully: {email}")
            return UserDTO.from_aggregate(user)
        except ValueError as e:
            self._logger.error(f"Authentication failed for {email}: {str(e)}")
            raise
        except Exception as e:
            self._logger.error(
                f"Unexpected error during authentication for {email}: {str(e)}"
            )
            raise ValueError("Failed to authenticate user") from e

    async def change_password(
        self, user_id: UUID, current_password: str, new_password: str
    ) -> None:
        """Change a user's password."""
        try:
            command = ChangePasswordCommand(
                user_id=user_id,
                current_password=current_password,
                new_password=new_password,
            )
            await self._change_password_handler.handle(command)
            self._logger.info(f"Password changed successfully for user: {user_id}")
        except ValueError as e:
            self._logger.error(f"Password change failed for user {user_id}: {str(e)}")
            raise
        except Exception as e:
            self._logger.error(
                f"Unexpected error during password change for user {user_id}: {str(e)}"
            )
            raise ValueError("Failed to change password") from e

    async def get_user_by_id(self, user_id: UUID) -> Optional[UserDTO]:
        """Get a user by their ID."""
        return await self._query_handler.get_by_id(GetUserByIdQuery(user_id=user_id))

    async def get_user_by_email(self, email: EmailStr) -> Optional[UserDTO]:
        """Get a user by their email."""
        return await self._query_handler.get_by_email(GetUserByEmailQuery(email=email))
