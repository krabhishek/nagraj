"""User-related specifications."""

from typing import Optional

from {{cookiecutter.project_slug}}.common.base.specification import BaseSpecification

from ..aggregates.user_aggregate import UserAggregate


class ActiveUserSpecification(BaseSpecification[UserAggregate]):
    """Specification for checking if a user is active."""

    def is_satisfied_by(self, user: UserAggregate) -> bool:
        """Check if the user is active."""
        return user.is_active


class UniqueEmailSpecification(BaseSpecification[str]):
    """Specification for checking if an email is unique."""

    def __init__(self, existing_email: Optional[str] = None):
        """Initialize with optional existing email for comparison."""
        self.existing_email = existing_email

    def is_satisfied_by(self, email: str) -> bool:
        """Check if the email is unique."""
        if not self.existing_email:
            return True
        return email.lower() != self.existing_email.lower()
