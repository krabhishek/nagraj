"""Command handlers for authentication operations."""

from {{cookiecutter.project_slug}}.common.bounded_contexts.auth.domain.aggregates.user_aggregate import (
    UserAggregate,
)
from {{cookiecutter.project_slug}}.common.bounded_contexts.auth.domain.services.user_authentication_service import (
    UserAuthenticationService,
)
from {{cookiecutter.project_slug}}.common.bounded_contexts.auth.domain.specifications.password_specifications import (
    ValidPasswordSpecification,
)
from {{cookiecutter.project_slug}}.common.bounded_contexts.auth.domain.specifications.user_specifications import (
    UniqueEmailSpecification,
)
from {{cookiecutter.project_slug}}.common.bounded_contexts.auth.infrastructure.repositories.user_repository import (
    UserRepository,
)
from {{cookiecutter.project_slug}}.common.core.events.event_dispatcher import EventDispatcher

from ..commands.authenticate_user import (
    AuthenticateUserCommand,
    AuthenticateUserHandler,
)
from ..commands.change_password import ChangePasswordCommand, ChangePasswordHandler
from ..commands.create_user import CreateUserCommand, CreateUserHandler
from ..dtos.user_dto import UserDTO
from ..queries.get_user import GetUserByEmailQuery, GetUserByIdQuery, UserQueryHandler


class UserCommandHandlers(
    CreateUserHandler, AuthenticateUserHandler, ChangePasswordHandler, UserQueryHandler
):
    """Handlers for user-related commands."""

    def __init__(
        self, repository: UserRepository, event_dispatcher: EventDispatcher
    ) -> None:
        """Initialize the handlers with a repository and event dispatcher."""
        self._repository = repository
        self._event_dispatcher = event_dispatcher
        self._auth_service = UserAuthenticationService()
        self._password_spec = ValidPasswordSpecification()

    async def handle(
        self,
        command: CreateUserCommand | AuthenticateUserCommand | ChangePasswordCommand,
    ) -> UserAggregate | None:
        """Handle commands based on their type."""
        if isinstance(command, CreateUserCommand):
            return await self.handle_create(command)
        elif isinstance(command, AuthenticateUserCommand):
            return await self.handle_authenticate(command)
        elif isinstance(command, ChangePasswordCommand):
            await self.handle_change_password(command)
            return None
        raise ValueError(f"Unknown command type: {type(command)}")

    async def handle_create(self, command: CreateUserCommand) -> UserAggregate:
        """Handle the create user command."""
        # Validate password
        if not self._password_spec.is_satisfied_by(command.password):
            raise ValueError("Password does not meet security requirements")

        # Check if user exists
        existing_user = await self._repository.get_by_email(str(command.email))
        email_spec = UniqueEmailSpecification(
            existing_email=existing_user.email.value if existing_user else None
        )

        if not email_spec.is_satisfied_by(str(command.email)):
            raise ValueError("User with this email already exists")

        # Create and save user
        user = UserAggregate.create(email=str(command.email), password=command.password)
        await self._repository.save(user)

        # Dispatch events
        for event in user.domain_events:
            await self._event_dispatcher.dispatch(event)

        return user

    async def handle_authenticate(
        self, command: AuthenticateUserCommand
    ) -> UserAggregate:
        """Handle the authenticate user command."""
        # Get user by email
        user = await self._repository.get_by_email(str(command.email))
        if not user:
            raise ValueError("Invalid email or password")

        # Validate authentication
        self._auth_service.validate_authentication(user, command.password)

        # Dispatch events
        for event in user.domain_events:
            await self._event_dispatcher.dispatch(event)

        return user

    async def handle_change_password(self, command: ChangePasswordCommand) -> None:
        """Handle the change password command."""
        # Get user by ID
        user = await self._repository.get_by_id(command.user_id)
        if not user:
            raise ValueError("User not found")

        # Validate password change
        self._auth_service.validate_password_change(
            user, command.current_password, command.new_password
        )

        # Change password and save
        user.change_password(command.current_password, command.new_password)
        await self._repository.save(user)

        # Dispatch events
        for event in user.domain_events:
            await self._event_dispatcher.dispatch(event)

    async def get_by_id(self, query: GetUserByIdQuery) -> UserDTO | None:
        """Handle the get user by ID query."""
        user = await self._repository.get_by_id(query.user_id)
        return UserDTO.from_aggregate(user) if user else None

    async def get_by_email(self, query: GetUserByEmailQuery) -> UserDTO | None:
        """Handle the get user by email query."""
        user = await self._repository.get_by_email(str(query.email))
        return UserDTO.from_aggregate(user) if user else None
