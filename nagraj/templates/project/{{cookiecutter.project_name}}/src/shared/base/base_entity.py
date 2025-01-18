"""Base entity class for domain entities."""

from datetime import UTC, datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class BaseEntity(BaseModel):
    """Base class for all domain entities."""

    model_config = ConfigDict(frozen=True)

    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: Optional[datetime] = None
    version: int = 1
