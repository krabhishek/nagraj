"""Base domain event class for domain events."""

from datetime import UTC, datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class BaseDomainEvent(BaseModel):
    """Base class for all domain events."""

    model_config = ConfigDict(frozen=True)

    id: UUID = Field(default_factory=uuid4)
    occurred_on: datetime = Field(default_factory=lambda: datetime.now(UTC))
    version: int = 1
    aggregate_id: Optional[UUID] = None
