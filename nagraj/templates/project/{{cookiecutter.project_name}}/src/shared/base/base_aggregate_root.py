"""Base aggregate root class for domain aggregates."""

{% set base_class = cookiecutter.base_classes.aggregate_root_base.split('.') %}
{% if base_class|length > 1 %}
from {{ '.'.join(base_class[:-1]) }} import {{ base_class[-1] }}
{% endif %}

from datetime import UTC, datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class BaseAggregateRoot({{ base_class[-1] }}):
    """Base class for all domain aggregate roots."""

    def __init__(self, *args, **kwargs):
        """Initialize the aggregate root."""
        super().__init__(*args, **kwargs)
        self._events = []

    def add_event(self, event: "BaseDomainEvent") -> None:
        """Add a domain event to the aggregate root."""
        self._events.append(event)

    def clear_events(self) -> None:
        """Clear all domain events from the aggregate root."""
        self._events = []

    @property
    def events(self) -> list["BaseDomainEvent"]:
        """Get all domain events from the aggregate root."""
        return self._events

    model_config = ConfigDict(frozen=True)

    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: Optional[datetime] = None
    version: int = 1

    def __eq__(self, other: object) -> bool:
        """Compare aggregates by their identity."""
        if not isinstance(other, BaseAggregateRoot):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        """Hash aggregate based on its identity."""
        return hash(self.id)
