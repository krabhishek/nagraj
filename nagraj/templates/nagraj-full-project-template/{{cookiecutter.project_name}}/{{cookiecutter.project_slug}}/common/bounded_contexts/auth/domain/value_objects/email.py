"""Email value object implementation."""

from dataclasses import dataclass

from {{cookiecutter.project_slug}}.common.base.value_object import BaseValueObject
from pydantic import BaseModel, EmailStr


class EmailValidator(BaseModel):
    """Email validator using Pydantic."""

    email: EmailStr


@dataclass(frozen=True)
class Email(BaseValueObject):
    """Email value object."""

    value: str

    def __str__(self) -> str:
        """Convert the email to a string."""
        return str(self.value)

    @classmethod
    def create(cls, value: str) -> "Email":
        """Create a new email value object."""
        # Validate email format
        EmailValidator(email=value)
        return cls(value=value)
