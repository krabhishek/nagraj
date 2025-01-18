"""Base domain event class for domain events."""

from datetime import UTC, datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class BaseDomainEvent(BaseModel):
    """Base class for all domain events."""

    model_config = ConfigDict(frozen=True)

    id: UUID = Field(default_factory=uuid4)
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    aggregate_id: Optional[UUID] = None
    version: int = 1

    def __eq__(self, other: object) -> bool:
        """Compare events by their identity."""
        if not isinstance(other, BaseDomainEvent):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        """Hash event based on its identity."""
        return hash(self.id)
