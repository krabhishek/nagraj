from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar
from uuid import UUID

from ..core.infrastructure.database.database import db

from .aggregate import BaseAggregate

T = TypeVar("T", bound=BaseAggregate)


class BaseRepository(ABC, Generic[T]):
    """
    Base class for Repository pattern implementation in DDD.

    Repositories mediate between the domain and data mapping layers,
    acting like in-memory domain object collections.
    """

    def __init__(self, schema: str):
        """Initialize repository with specific schema."""
        self._schema = schema
        self._initialized = False

    async def _ensure_initialized(self) -> None:
        """Ensure the database connection is initialized with the correct schema."""
        if not self._initialized:
            await db.create_pool(schema=self._schema)
            self._initialized = True

    @abstractmethod
    async def save(self, aggregate: T) -> None:
        """
        Persists the aggregate to the storage.

        Args:
            aggregate: The aggregate root to save
        """
        await self._ensure_initialized()
        pass

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Optional[T]:
        """
        Retrieves an aggregate by its ID.

        Args:
            id: The unique identifier of the aggregate

        Returns:
            The aggregate if found, None otherwise
        """
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> None:
        """
        Removes an aggregate from storage.

        Args:
            id: The unique identifier of the aggregate to delete
        """
        await self._ensure_initialized()
        pass
