"""Event dispatcher implementation."""

from typing import Awaitable, Callable, Dict, List, Type

from ...base.domain_event import BaseDomainEvent

EventHandler = Callable[[BaseDomainEvent], Awaitable[None]]


class EventDispatcher:
    """Event dispatcher for handling domain events."""

    def __init__(self) -> None:
        """Initialize the event dispatcher."""
        self._handlers: Dict[Type[BaseDomainEvent], List[EventHandler]] = {}

    def register(
        self, event_type: Type[BaseDomainEvent], handler: EventHandler
    ) -> None:
        """Register a handler for an event type."""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    async def dispatch(self, event: BaseDomainEvent) -> None:
        """Dispatch an event to all registered handlers."""
        event_type = type(event)
        if event_type in self._handlers:
            for handler in self._handlers[event_type]:
                await handler(event)

    def clear_handlers(self) -> None:
        """Clear all registered handlers."""
        self._handlers.clear()
