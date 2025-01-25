"""User entity representing an authenticated user in the system."""

from datetime import datetime, timezone
from typing import Optional

from pydantic import Field

from {{cookiecutter.project_slug}}.common.base.entity import BaseEntity


class User(BaseEntity):
    """User entity representing an authenticated user in the system."""

    email: str = Field(description="User's email address")
    password_hash: str = Field(description="User's hashed password")
    is_active: bool = Field(
        default=True, description="Whether the user account is active"
    )
    last_login: Optional[datetime] = Field(
        default=None, description="Timestamp of user's last login"
    )

    def update_last_login(self) -> None:
        """Update the last login timestamp."""
        self.last_login = datetime.now(timezone.utc)

    def deactivate(self) -> None:
        """Deactivate the user account."""
        self.is_active = False

    def activate(self) -> None:
        """Activate the user account."""
        self.is_active = True
