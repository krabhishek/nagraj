"""Base facade implementation for bounded context integration."""

from abc import ABC
from typing import Any, Dict, Generic, TypeVar

from .aggregate import BaseAggregate

T = TypeVar("T", bound=BaseAggregate)


class BaseFacade(Generic[T], ABC):
    """
    Base class for bounded context facades.

    Facades provide a simplified interface to a bounded context,
    hiding its internal complexity and providing translation
    between different bounded contexts.
    """

    def __init__(self) -> None:
        """Initialize the facade."""
        self._context_data: Dict[str, Any] = {}

    def set_context_data(self, key: str, value: Any) -> None:
        """Set context-specific data."""
        self._context_data[key] = value

    def get_context_data(self, key: str) -> Any:
        """Get context-specific data."""
        return self._context_data.get(key)
