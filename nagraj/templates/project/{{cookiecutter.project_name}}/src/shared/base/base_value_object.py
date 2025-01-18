"""Base value object class for domain value objects."""

from pydantic import BaseModel, ConfigDict


class BaseValueObject(BaseModel):
    """Base class for all value objects."""

    model_config = ConfigDict(frozen=True)

    def __eq__(self, other: object) -> bool:
        """Compare value objects by their values."""
        if not isinstance(other, BaseValueObject):
            return NotImplemented
        return self.model_dump() == other.model_dump()
