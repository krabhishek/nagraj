"""User aggregate implementation."""

from datetime import datetime, timezone
from typing import List, Self
from uuid import UUID, uuid4

from {{cookiecutter.project_slug}}.common.base.aggregate import BaseAggregate
from {{cookiecutter.project_slug}}.common.base.domain_event import BaseDomainEvent
from pydantic import Field, model_validator

from ..entities.user import User
from ..events.user_events import (
    PasswordChangedEvent,
    UserActivatedEvent,
    UserCreatedEvent,
    UserDeactivatedEvent,
)
from ..specifications.password_specifications import ValidPasswordSpecification
from ..value_objects.email import Email
from ..value_objects.password import Password


class UserAggregate(BaseAggregate):
    """User Aggregate Root that encapsulates user-related domain logic and enforces invariants."""

    email: Email = Field(description="User's email address")
    password: Password = Field(description="User's hashed password")
    is_active: bool = Field(
        default=True, description="Whether the user account is active"
    )
    last_login: datetime | None = Field(
        default=None, description="Timestamp of user's last login"
    )

    def __init__(
        self,
        id: UUID,
        email: Email,
        password: Password,
        is_active: bool,
        created_at: datetime,
        updated_at: datetime,
        domain_events: List[BaseDomainEvent],
    ) -> None:
        """Initialize a user aggregate."""
        super().__init__(
            id=id,
            email=email,
            password=password,
            is_active=is_active,
            created_at=created_at,
            updated_at=updated_at,
            domain_events=domain_events,
        )

    @classmethod
    def create(cls, email: str, password: str) -> "UserAggregate":
        """Create a new user aggregate."""
        now = datetime.now(timezone.utc)
        email_vo = Email.create(email)
        password_validator = ValidPasswordSpecification()
        password_vo = Password(password, validator=password_validator)

        # Create the aggregate
        aggregate = cls(
            id=uuid4(),
            email=email_vo,
            password=password_vo,
            is_active=True,
            created_at=now,
            updated_at=now,
            domain_events=[],
        )

        # Add creation event
        event = UserCreatedEvent.create(
            aggregate_id=aggregate.id,
            email=str(email_vo),
            is_active=True,
        )
        aggregate.add_domain_event(event)

        return aggregate

    @property
    def email_str(self) -> str:
        """Get the user's email as a string."""
        return str(self.email)

    def verify_password(self, password: str) -> bool:
        """Verify if the provided password matches."""
        return self.password.verify(password)

    def change_password(self, current_password: str, new_password: str) -> None:
        """Change the user's password."""
        if not self.verify_password(current_password):
            raise ValueError("Current password is incorrect")

        password_validator = ValidPasswordSpecification()
        new_password_vo = Password(new_password, validator=password_validator)
        self.password = new_password_vo
        self._update_timestamp()

        event = PasswordChangedEvent.create(
            aggregate_id=self.id,
            email=self.email_str,
        )
        self.add_domain_event(event)

    def update_last_login(self, timestamp: datetime) -> None:
        """Update the last login timestamp."""
        self.last_login = timestamp
        self._update_timestamp()

    def deactivate(self) -> None:
        """Deactivate the user."""
        if not self.is_active:
            raise ValueError("User is already inactive")

        self.is_active = False
        self._update_timestamp()

        event = UserDeactivatedEvent.create(
            aggregate_id=self.id,
            email=self.email_str,
        )
        self.add_domain_event(event)

    def activate(self) -> None:
        """Activate the user."""
        if self.is_active:
            raise ValueError("User is already active")

        self.is_active = True
        self._update_timestamp()

        event = UserActivatedEvent.create(
            aggregate_id=self.id,
            email=self.email_str,
        )
        self.add_domain_event(event)

    def _update_timestamp(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now(timezone.utc)

    def to_entity(self) -> User:
        """Convert aggregate to entity for persistence."""
        return User(
            id=self.id,
            email=self.email_str,
            password_hash=self.password.hashed_value,
            is_active=self.is_active,
            last_login=self.last_login,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @model_validator(mode="after")
    def validate_invariants(self) -> Self:
        """Validate user aggregate invariants."""
        if not self.email:
            raise ValueError("Email is required")
        if not self.password:
            raise ValueError("Password is required")
        return self
