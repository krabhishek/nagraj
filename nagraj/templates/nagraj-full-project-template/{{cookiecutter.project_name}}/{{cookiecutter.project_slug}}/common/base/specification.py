"""Base specification pattern implementation."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class BaseSpecification(Generic[T], ABC):
    """Base class for specifications."""

    @abstractmethod
    def is_satisfied_by(self, candidate: T) -> bool:
        """Check if the candidate satisfies the specification."""
        pass

    def and_(self, other: "BaseSpecification[T]") -> "AndSpecification[T]":
        """Combine with another specification using AND."""
        return AndSpecification(self, other)

    def or_(self, other: "BaseSpecification[T]") -> "OrSpecification[T]":
        """Combine with another specification using OR."""
        return OrSpecification(self, other)

    def not_(self) -> "NotSpecification[T]":
        """Negate this specification."""
        return NotSpecification(self)


class AndSpecification(BaseSpecification[T]):
    """Specification that combines two specifications with AND."""

    def __init__(
        self, spec1: BaseSpecification[T], spec2: BaseSpecification[T]
    ) -> None:
        self._spec1 = spec1
        self._spec2 = spec2

    def is_satisfied_by(self, candidate: T) -> bool:
        """Check if both specifications are satisfied."""
        return self._spec1.is_satisfied_by(candidate) and self._spec2.is_satisfied_by(
            candidate
        )


class OrSpecification(BaseSpecification[T]):
    """Specification that combines two specifications with OR."""

    def __init__(
        self, spec1: BaseSpecification[T], spec2: BaseSpecification[T]
    ) -> None:
        self._spec1 = spec1
        self._spec2 = spec2

    def is_satisfied_by(self, candidate: T) -> bool:
        """Check if either specification is satisfied."""
        return self._spec1.is_satisfied_by(candidate) or self._spec2.is_satisfied_by(
            candidate
        )


class NotSpecification(BaseSpecification[T]):
    """Specification that negates another specification."""

    def __init__(self, spec: BaseSpecification[T]) -> None:
        self._spec = spec

    def is_satisfied_by(self, candidate: T) -> bool:
        """Check if the specification is not satisfied."""
        return not self._spec.is_satisfied_by(candidate)
