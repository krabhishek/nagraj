from abc import ABC
from dataclasses import dataclass, fields


@dataclass(frozen=True)  # Ensures immutability
class BaseValueObject(ABC):
    """
    Base class for Value Objects in a Domain-Driven Design (DDD) project.
    Value Objects are immutable and equality is based on their state, not identity.
    """

    def __eq__(self, other: object) -> bool:
        """
        Compare two Value Objects for equality based on their attributes.

        Returns False if other is not a value object or has different attributes.
        """
        if not isinstance(other, BaseValueObject):
            return False
        return all(
            getattr(self, field.name) == getattr(other, field.name)
            for field in fields(self)
        )

    def __hash__(self) -> int:
        """
        Generate a hash based on the Value Object's attributes.
        This ensures Value Objects can be used in sets and as dictionary keys.
        """
        return hash(tuple(getattr(self, field.name) for field in fields(self)))

    def __repr__(self) -> str:
        """
        Provide a string representation of the Value Object for debugging.
        """
        attributes = ", ".join(
            f"{field.name}={getattr(self, field.name)!r}" for field in fields(self)
        )
        return f"{self.__class__.__name__}({attributes})"
