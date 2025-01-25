from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

import pytest
from {{cookiecutter.project_slug}}.common.bounded_contexts.auth.application.commands.authenticate_user import (
    AuthenticateUserCommand,
    AuthenticateUserHandler,
)
from {{cookiecutter.project_slug}}.common.bounded_contexts.auth.application.commands.change_password import (
    ChangePasswordCommand,
    ChangePasswordHandler,
)
from {{cookiecutter.project_slug}}.common.bounded_contexts.auth.application.commands.create_user import (
    CreateUserCommand,
    CreateUserHandler,
)
from {{cookiecutter.project_slug}}.common.bounded_contexts.auth.application.queries.get_user import (
    GetUserByEmailQuery,
    GetUserByIdQuery,
    UserQueryHandler,
)
from {{cookiecutter.project_slug}}.common.bounded_contexts.auth.application.services.auth_service import (
    AuthService as DefaultAuthService,
)
from {{cookiecutter.project_slug}}.common.bounded_contexts.auth.domain.aggregates.user_aggregate import (
    UserAggregate,
)


class MockCreateUserHandler(CreateUserHandler):
    """Mock implementation of CreateUserHandler."""

    async def handle(self, command: CreateUserCommand) -> UserAggregate:
        user = UserAggregate.create(
            email=str(command.email),
            password=command.password,
        )
        return user


class MockAuthenticateUserHandler(AuthenticateUserHandler):
    """Mock implementation of AuthenticateUserHandler."""

    def __init__(self, should_succeed: bool = True):
        """Initialize the handler."""
        self.should_succeed = should_succeed

    async def handle(self, command: AuthenticateUserCommand) -> UserAggregate:
        user = UserAggregate.create(
            email=str(command.email),
            password="Test@123456",  # Use a valid password
        )

        if not self.should_succeed:
            raise ValueError("Failed to authenticate user")

        user.update_last_login(datetime.now(timezone.utc))
        return user


class MockChangePasswordHandler(ChangePasswordHandler):
    """Mock implementation of ChangePasswordHandler."""

    async def handle(self, command: ChangePasswordCommand) -> None:
        if command.current_password == "wrong":
            raise ValueError("Current password is incorrect")


class MockUserQueryHandler(UserQueryHandler):
    """Mock implementation of UserQueryHandler."""

    def __init__(self, existing_user: Optional[UserAggregate] = None):
        """Initialize the handler."""
        self.existing_user = existing_user

    async def get_by_id(self, query: GetUserByIdQuery) -> Optional[UserAggregate]:
        """Get user by ID."""
        return self.existing_user

    async def get_by_email(self, query: GetUserByEmailQuery) -> Optional[UserAggregate]:
        """Get user by email."""
        if query.email == "existing@example.com":
            return UserAggregate.create(
                email=str(query.email),
                password="Test@123456",  # Use a valid password
            )
        return None


@pytest.fixture
def auth_service():
    """Fixture for auth service."""
    return DefaultAuthService(
        create_user_handler=MockCreateUserHandler(),
        authenticate_user_handler=MockAuthenticateUserHandler(),
        change_password_handler=MockChangePasswordHandler(),
        query_handler=MockUserQueryHandler(),
    )


@pytest.fixture
def auth_service_with_existing_user():
    """Fixture for auth service with an existing user."""
    existing_user = UserAggregate.create(
        email="existing@example.com",
        password="Test@123456",  # Use a valid password
    )
    return DefaultAuthService(
        create_user_handler=MockCreateUserHandler(),
        authenticate_user_handler=MockAuthenticateUserHandler(),
        change_password_handler=MockChangePasswordHandler(),
        query_handler=MockUserQueryHandler(existing_user=existing_user),
    )


@pytest.mark.asyncio
async def test_register_new_user(auth_service):
    """Test registering a new user."""
    user_dto = await auth_service.register_user(
        email="test@example.com",
        password="Test@123456",  # Use a valid password
    )

    assert user_dto is not None
    assert user_dto.email == "test@example.com"
    assert user_dto.is_active is True


@pytest.mark.asyncio
async def test_register_existing_user(auth_service_with_existing_user):
    """Test registering a user with an existing email."""
    with pytest.raises(ValueError, match="User with this email already exists"):
        await auth_service_with_existing_user.register_user(
            email="existing@example.com",
            password="Test@123456",  # Use a valid password
        )


@pytest.mark.asyncio
async def test_authenticate_user_success(auth_service):
    """Test successful user authentication."""
    user_dto = await auth_service.authenticate_user(
        email="test@example.com",
        password="Test@123456",  # Use a valid password
    )

    assert user_dto is not None
    assert user_dto.email == "test@example.com"
    assert user_dto.last_login is not None


@pytest.mark.asyncio
async def test_authenticate_user_failure():
    """Test failed user authentication."""
    service = DefaultAuthService(
        create_user_handler=MockCreateUserHandler(),
        authenticate_user_handler=MockAuthenticateUserHandler(should_succeed=False),
        change_password_handler=MockChangePasswordHandler(),
        query_handler=MockUserQueryHandler(),
    )

    with pytest.raises(ValueError, match="Failed to authenticate user"):
        await service.authenticate_user(
            email="test@example.com",
            password="Test@123456",  # Use a valid password
        )


@pytest.mark.asyncio
async def test_change_password_success(auth_service):
    """Test successful password change."""
    await auth_service.change_password(
        user_id=uuid4(),
        current_password="Test@123456",  # Use a valid password
        new_password="NewTest@123456",  # Use a valid password
    )


@pytest.mark.asyncio
async def test_change_password_failure(auth_service):
    """Test failed password change."""
    with pytest.raises(ValueError, match="Current password is incorrect"):
        await auth_service.change_password(
            user_id=uuid4(),
            current_password="wrong",
            new_password="NewTest@123456",  # Use a valid password
        )
