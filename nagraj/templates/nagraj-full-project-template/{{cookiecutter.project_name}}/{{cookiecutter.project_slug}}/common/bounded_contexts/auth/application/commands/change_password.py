from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID


@dataclass
class ChangePasswordCommand:
    """Command to change a user's password."""

    user_id: UUID
    current_password: str
    new_password: str


class ChangePasswordHandler(ABC):
    """Handler for password changes."""

    @abstractmethod
    async def handle(self, command: ChangePasswordCommand) -> None:
        """Handle the change password command."""
        pass
