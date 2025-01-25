"""User authentication domain service."""

from datetime import datetime, timezone

from {{cookiecutter.project_slug}}.common.base.domain_service import BaseDomainService
from {{cookiecutter.project_slug}}.common.core.logging import LoggerService

from ..aggregates.user_aggregate import UserAggregate
from ..events.user_events import UserAuthenticatedEvent
from ..specifications.password_specifications import ValidPasswordSpecification
from ..specifications.user_specifications import (
    ActiveUserSpecification,
)


class UserAuthenticationService(BaseDomainService[UserAggregate]):
    """Domain service for user authentication."""

    def __init__(self) -> None:
        """Initialize the service."""
        super().__init__()
        self._logger = LoggerService().get_logger({"module": "user_auth_service"})
        self._active_user_spec = ActiveUserSpecification()
        self._valid_password_spec = ValidPasswordSpecification()

    def authenticate_user(self, user: UserAggregate, password: str) -> bool:
        """Authenticate a user and handle related business logic."""
        # Check if user is active
        if not self._active_user_spec.is_satisfied_by(user):
            raise ValueError("Account is inactive")

        # Verify password
        if not user.verify_password(password):
            return False

        # Update last login
        user.update_last_login(datetime.now(timezone.utc))

        # Add authentication event
        event = UserAuthenticatedEvent.create(
            aggregate_id=user.id,
            email=user.email_str,
        )
        user.add_domain_event(event)

        return True

    def validate_password_change(
        self, user: UserAggregate, current_password: str, new_password: str
    ) -> None:
        """Validate password change according to domain rules."""
        # Check if user is active
        if not self._active_user_spec.is_satisfied_by(user):
            raise ValueError("Inactive users cannot change their password")

        # Verify current password
        if not user.verify_password(current_password):
            raise ValueError("Current password is incorrect")

        # Validate new password
        if not self._valid_password_spec.is_satisfied_by(new_password):
            raise ValueError("New password does not meet security requirements")

        # Check if new password is different
        if current_password == new_password:
            raise ValueError("New password must be different from current password")

    def validate_authentication(self, user: UserAggregate, password: str) -> None:
        """Validate user authentication according to domain rules."""
        # Check if user is active
        if not self._active_user_spec.is_satisfied_by(user):
            raise ValueError("Account is inactive")

        # Verify password
        if not user.verify_password(password):
            raise ValueError("Invalid password")
