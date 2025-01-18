"""Base aggregate root class for domain aggregates."""

from typing import List

from .base_domain_event import BaseDomainEvent
from .base_entity import BaseEntity


class BaseAggregateRoot(BaseEntity):
    """Base class for all aggregate roots."""

    def __init__(self, **data):
        super().__init__(**data)
        self._events: List[BaseDomainEvent] = []

    def add_event(self, event: BaseDomainEvent) -> None:
        """Add a domain event to the aggregate."""
        self._events.append(event)

    def clear_events(self) -> List[BaseDomainEvent]:
        """Clear and return all pending domain events."""
        events = self._events[:]
        self._events.clear()
        return events
