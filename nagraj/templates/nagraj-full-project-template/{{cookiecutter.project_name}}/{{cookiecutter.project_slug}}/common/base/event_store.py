"""Base event store implementation."""

from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from .domain_event import BaseDomainEvent


class BaseEventStore(ABC):
    """Base class for event stores."""

    @abstractmethod
    async def append_events(self, events: List[BaseDomainEvent]) -> None:
        """Append events to the store."""
        pass

    @abstractmethod
    async def get_events(self, aggregate_id: UUID) -> List[BaseDomainEvent]:
        """Get all events for an aggregate."""
        pass

    @abstractmethod
    async def get_events_since(
        self, aggregate_id: UUID, since_version: int
    ) -> List[BaseDomainEvent]:
        """Get events for an aggregate since a specific version."""
        pass
