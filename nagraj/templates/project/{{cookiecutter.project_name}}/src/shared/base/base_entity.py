"""Base entity class for domain entities."""

from pydantic import BaseModel


class BaseEntity(BaseModel):
    """Base class for all domain entities."""

    def __eq__(self, other: object) -> bool:
        """Compare entities by their identity."""
        if not isinstance(other, BaseEntity):
            return NotImplemented
        return self.model_dump() == other.model_dump()

    def __hash__(self) -> int:
        """Hash entity based on its identity."""
        return hash(tuple(sorted(self.model_dump().items())))
