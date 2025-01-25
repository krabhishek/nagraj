from abc import ABC, abstractmethod

from .domain_event import BaseDomainEvent


class BaseEventHandler(ABC):
    """Base class for domain event handlers."""

    @abstractmethod
    async def handle(self, event: BaseDomainEvent) -> None:
        """Handle a domain event."""
        pass
