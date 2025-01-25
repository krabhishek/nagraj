"""Base domain service implementation."""

from abc import ABC
from typing import Generic, TypeVar

from .aggregate import BaseAggregate

T = TypeVar("T", bound=BaseAggregate)


class BaseDomainService(Generic[T], ABC):
    """
    Base class for domain services.

    Domain services encapsulate complex business logic that doesn't naturally
    fit within a single aggregate or value object. They are stateless and
    operate on one or more aggregates.
    """

    def __init__(self) -> None:
        """Initialize the domain service."""
        pass

    def validate_business_rules(self, aggregate: T) -> None:
        """
        Validates complex business rules that span multiple aggregates
        or require external services.

        Args:
            aggregate: The aggregate to validate

        Raises:
            ValueError: If business rules are violated
        """
        pass
