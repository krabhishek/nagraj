"""Base domain event class."""

from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    field_validator,
    model_validator,
)


class BaseDomainEvent(BaseModel):
    """
    Base Class for Domain Events

    Domain events represent something meaningful that happened in the domain. They are immutable
    and typically used to communicate changes across different parts of the system, such as in
    event sourcing or CQRS architectures.
    """

    model_config = ConfigDict(frozen=True)

    event_id: UUID = Field(default_factory=uuid4)
    aggregate_id: UUID = Field(description="ID of the aggregate this event belongs to")
    occurred_on: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    event_type: str = Field(default="")
    event_version: int = Field(default=1)

    @model_validator(mode="before")
    def set_event_type(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Set the event type to the class name if not provided."""
        if "event_type" not in values or not values["event_type"]:
            values["event_type"] = cls.__name__
        return values

    @field_validator("occurred_on", mode="before")
    @classmethod
    def validate_occurred_on(cls, value: Any) -> datetime:
        """Validate that occurred_on is a timezone-aware datetime."""
        if isinstance(value, str):
            try:
                value = datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                raise ValueError("occurred_on must be a valid ISO format datetime")
        if not isinstance(value, datetime):
            raise ValueError("occurred_on must be a datetime")
        if value.tzinfo is None:
            raise ValueError("Datetime must be timezone-aware")
        return value

    def __eq__(self, other: object) -> bool:
        """Compare two domain events for equality based on their event_id."""
        if not isinstance(other, BaseDomainEvent):
            return False
        return self.event_id == other.event_id

    def __hash__(self) -> int:
        """Generate a hash based on the event_id."""
        return hash(self.event_id)

    def __repr__(self) -> str:
        """
        String representation of the domain event.

        Returns:
            str: A string representation of the domain event.
        """
        return f"{self.__class__.__name__}(event_id={self.event_id}, event_type={self.event_type})"

    @classmethod
    def from_json(cls, json_str: str) -> "BaseDomainEvent":
        """Create a domain event from a JSON string."""
        try:
            return cls.model_validate_json(json_str)
        except ValidationError as e:
            raise ValueError(f"Failed to deserialize domain event: {str(e)}")
        except Exception as e:
            raise ValueError(f"Failed to deserialize domain event: {str(e)}")

    def model_dump_json(self, **kwargs: Any) -> str:
        """Override model_dump_json to handle datetime serialization."""
        kwargs.setdefault("exclude_none", True)
        return super().model_dump_json(**kwargs)
