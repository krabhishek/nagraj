from typing import Self, TypeVar

from pydantic import model_validator

from .entity import BaseEntity

T = TypeVar("T", bound="BaseAggregate")


class BaseAggregate(BaseEntity):
    """
    Base class for Aggregate Roots in Domain-Driven Design.

    Aggregates are clusters of domain objects that can be treated as a single unit.
    They enforce consistency boundaries and encapsulate domain rules that apply to
    the cluster as a whole.
    """

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self._version: int = 1

    @property
    def version(self) -> int:
        """
        Returns the current version of the aggregate.
        Used for optimistic concurrency control.
        """
        return self._version

    def increment_version(self) -> None:
        """
        Increments the aggregate version.
        Should be called when the aggregate state changes.
        """
        self._version += 1

    @classmethod
    def create(cls: type[T], **kwargs) -> T:
        """
        Factory method to create a new aggregate instance.
        Override this in concrete aggregate classes to enforce invariants.
        """
        return cls(**kwargs)

    @model_validator(mode="before")
    def validate_invariants(self) -> Self:
        """
        Validates the aggregate's invariants.
        Override this in concrete aggregate classes to implement specific validation rules.

        Raises:
            ValueError: If any invariants are violated
        """
        raise NotImplementedError(
            "Subclass must implement the `validate_invariants` method"
        )
