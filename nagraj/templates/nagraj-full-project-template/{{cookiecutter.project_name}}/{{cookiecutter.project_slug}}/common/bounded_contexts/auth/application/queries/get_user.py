from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from pydantic import EmailStr

from ..dtos.user_dto import UserDTO


@dataclass
class GetUserByIdQuery:
    """Query to get a user by ID."""

    user_id: UUID


@dataclass
class GetUserByEmailQuery:
    """Query to get a user by email."""

    email: EmailStr


class UserQueryHandler(ABC):
    """Handler for user queries."""

    @abstractmethod
    async def get_by_id(self, query: GetUserByIdQuery) -> Optional[UserDTO]:
        """Handle the get user by ID query."""
        pass

    @abstractmethod
    async def get_by_email(self, query: GetUserByEmailQuery) -> Optional[UserDTO]:
        """Handle the get user by email query."""
        pass
