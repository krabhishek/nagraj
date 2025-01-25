"""Domain events for the user aggregate."""

from uuid import UUID

from {{cookiecutter.project_slug}}.common.base.domain_event import BaseDomainEvent


class UserCreatedEvent(BaseDomainEvent):
    """Event emitted when a user is created."""

    email: str
    is_active: bool

    @classmethod
    def create(
        cls, aggregate_id: UUID, email: str, is_active: bool
    ) -> "UserCreatedEvent":
        """Create a new user created event."""
        return cls(
            aggregate_id=aggregate_id,
            email=email,
            is_active=is_active,
        )


class UserAuthenticatedEvent(BaseDomainEvent):
    """Event emitted when a user is authenticated."""

    email: str

    @classmethod
    def create(cls, aggregate_id: UUID, email: str) -> "UserAuthenticatedEvent":
        """Create a new user authenticated event."""
        return cls(
            aggregate_id=aggregate_id,
            email=email,
        )


class UserDeactivatedEvent(BaseDomainEvent):
    """Event emitted when a user is deactivated."""

    email: str

    @classmethod
    def create(cls, aggregate_id: UUID, email: str) -> "UserDeactivatedEvent":
        """Create a new user deactivated event."""
        return cls(
            aggregate_id=aggregate_id,
            email=email,
        )


class UserActivatedEvent(BaseDomainEvent):
    """Event emitted when a user is activated."""

    email: str

    @classmethod
    def create(cls, aggregate_id: UUID, email: str) -> "UserActivatedEvent":
        """Create a new user activated event."""
        return cls(
            aggregate_id=aggregate_id,
            email=email,
        )


class PasswordChangedEvent(BaseDomainEvent):
    """Event emitted when a user's password is changed."""

    email: str

    @classmethod
    def create(cls, aggregate_id: UUID, email: str) -> "PasswordChangedEvent":
        """Create a new password changed event."""
        return cls(
            aggregate_id=aggregate_id,
            email=email,
        )
