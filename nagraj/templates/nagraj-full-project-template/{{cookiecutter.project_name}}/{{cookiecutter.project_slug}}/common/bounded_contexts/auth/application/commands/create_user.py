from abc import ABC, abstractmethod
from dataclasses import dataclass

from pydantic import EmailStr

from ...domain.aggregates.user_aggregate import UserAggregate


@dataclass
class CreateUserCommand:
    """Command to create a new user."""

    email: EmailStr
    password: str


class CreateUserHandler(ABC):
    """Handler for user creation."""

    @abstractmethod
    async def handle(self, command: CreateUserCommand) -> UserAggregate:
        """Handle the create user command."""
        pass
