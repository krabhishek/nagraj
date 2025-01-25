from datetime import datetime, timezone
from typing import Any, Self
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic.config import ConfigDict

from .domain_event import BaseDomainEvent


class BaseEntity(BaseModel):
    """
    Domain Entity Base Class

    This module defines the base class for domain entities in a domain-driven design (DDD)
    architecture. Entities represent stateful concepts within the domain, defined by a unique
    identity (`id`) rather than their attributes. They encapsulate behavior and can change
    state over time while maintaining domain invariants.
    """

    id: UUID = Field(
        default_factory=uuid4,
        description="Unique identifier for the entity",
        frozen=True,
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC timestamp of when the entity was first created",
        frozen=True,
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC timestamp of when the entity was last updated",
        frozen=False,
    )
    domain_events: list[BaseDomainEvent] = Field(
        default_factory=list,
        description="List of domain events that have occurred on this entity",
        frozen=False,
    )

    # Use the new ConfigDict to configure validation behavior
    model_config = ConfigDict(validate_assignment=True, extra="forbid")

    @model_validator(mode="after")
    def update_timestamps(self) -> Self:
        """
        Automatically updates the `updated_at` field whenever the model is validated.

        Returns:
            BaseEntity: The validated entity with an updated `updated_at` timestamp.
        """
        self.model_config["validate_assignment"] = False
        self.updated_at = datetime.now(timezone.utc)
        self.model_config["validate_assignment"] = True
        return self

    @field_validator("created_at", "updated_at", mode="before")
    @classmethod
    def validate_datetime(cls, value: Any) -> datetime:
        """
        Validates and ensures that `created_at` and `updated_at` are timezone-aware datetimes.

        Args:
            value (Any): The value to validate.

        Returns:
            datetime: A valid timezone-aware datetime.
        """
        if not isinstance(value, datetime):
            raise ValueError("Invalid datetime format")
        if value.tzinfo is None:
            raise ValueError("Datetime must be timezone-aware")
        return value

    def __eq__(self, other: object) -> bool:
        """
        Compare entities by their unique ID.

        Args:
            other (object): The object to compare with.

        Returns:
            bool: True if the IDs match, otherwise False.
        """
        if isinstance(other, BaseEntity):
            return self.id == other.id
        return False

    def __hash__(self) -> int:
        """
        Generate a hash based on the entity's unique ID.

        Returns:
            int: The hash of the entity's ID.
        """
        return hash(self.id)

    def __repr__(self) -> str:
        """
        String representation of the entity.

        Returns:
            str: A string representation of the entity.
        """
        return f"{self.__class__.__name__}(id={self.id})"

    def model_dump(self, **kwargs) -> dict:
        """
        Serialize the entity to a dictionary using Pydantic's model_dump method.

        Returns:
            dict: The serialized entity.
        """
        return super().model_dump(**kwargs)

    def add_domain_event(self, event: BaseDomainEvent) -> None:
        """
        Adds a domain event to the entity.

        Args:
            event (BaseDomainEvent): The domain event to add.
        """
        self.domain_events.append(event)

    def clear_domain_events(self) -> None:
        """
        Clears all domain events for the entity.
        """
        self.domain_events.clear()
