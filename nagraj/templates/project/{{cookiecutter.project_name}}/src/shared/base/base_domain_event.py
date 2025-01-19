"""Base domain event class for domain events."""

{% set base_class = cookiecutter.base_classes.entity_base.split('.') %}
{% if base_class|length > 1 %}
from {{ '.'.join(base_class[:-1]) }} import {{ base_class[-1] }}
{% endif %}

from datetime import UTC, datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class BaseDomainEvent({{ base_class[-1] }}):
    """Base class for all domain events."""

    model_config = ConfigDict(frozen=True)

    id: UUID = Field(default_factory=uuid4)
    occurred_at: datetime = datetime.now(UTC)
    aggregate_id: Optional[UUID] = None
    version: int = 1

    def __eq__(self, other: object) -> bool:
        """Compare domain events by their values."""
        if not isinstance(other, BaseDomainEvent):
            return NotImplemented
        return self.model_dump() == other.model_dump()

    def __hash__(self) -> int:
        """Hash domain event based on its values."""
        return hash(tuple(sorted(self.model_dump().items())))
