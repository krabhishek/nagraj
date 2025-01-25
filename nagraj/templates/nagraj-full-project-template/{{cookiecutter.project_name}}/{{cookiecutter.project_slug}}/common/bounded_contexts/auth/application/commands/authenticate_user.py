from abc import ABC, abstractmethod
from dataclasses import dataclass

from pydantic import EmailStr

from ...domain.aggregates.user_aggregate import UserAggregate


@dataclass
class AuthenticateUserCommand:
    """Command to authenticate a user."""

    email: EmailStr
    password: str


class AuthenticateUserHandler(ABC):
    """Handler for user authentication."""

    @abstractmethod
    async def handle(self, command: AuthenticateUserCommand) -> UserAggregate:
        """Handle the authenticate user command."""
        pass
