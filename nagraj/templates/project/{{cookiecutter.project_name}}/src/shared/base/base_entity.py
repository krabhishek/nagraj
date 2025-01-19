"""Base entity class for domain entities."""

{% set base_class = cookiecutter.base_classes.entity_base.split('.') %}
{% if base_class|length > 1 %}
from {{ '.'.join(base_class[:-1]) }} import {{ base_class[-1] }}
{% endif %}


class BaseEntity({{ base_class[-1] }}):
    """Base class for all domain entities."""

    def __eq__(self, other: object) -> bool:
        """Compare entities by their identity."""
        if not isinstance(other, BaseEntity):
            return NotImplemented
        return self.model_dump() == other.model_dump()

    def __hash__(self) -> int:
        """Hash entity based on its identity."""
        return hash(tuple(sorted(self.model_dump().items())))
