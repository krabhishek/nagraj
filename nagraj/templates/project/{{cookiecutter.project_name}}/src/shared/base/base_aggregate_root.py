"""Base aggregate root class for domain aggregates."""

from datetime import UTC, datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class BaseAggregateRoot(BaseModel):
    """Base class for all domain aggregates."""

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
