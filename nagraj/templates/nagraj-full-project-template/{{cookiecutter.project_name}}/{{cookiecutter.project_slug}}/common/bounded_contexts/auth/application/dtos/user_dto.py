"""User DTO for application layer."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr

from ...domain.aggregates.user_aggregate import UserAggregate


class UserDTO(BaseModel):
    """User data transfer object."""

    id: UUID
    email: EmailStr
    is_active: bool = True  # Default to True since we don't have user deactivation yet
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None

    @classmethod
    def from_aggregate(cls, aggregate: UserAggregate) -> "UserDTO":
        """Create a DTO from a user aggregate."""
        return cls(
            id=aggregate.id,
            email=str(aggregate.email),  # Convert Email value object to string
            is_active=aggregate.is_active,
            created_at=aggregate.created_at,
            updated_at=aggregate.updated_at,
            last_login=aggregate.last_login,
        )

    @classmethod
    def model_validate(cls, obj):
        """Convert from UserAggregate to UserDTO."""
        return cls(
            id=obj.id,
            email=obj.email.value,  # Access the actual email value
            is_active=True,  # Default to True since we don't have user deactivation yet
            created_at=obj.created_at,
            updated_at=obj.updated_at,
            last_login=obj.last_login,
        )
