"""Base value object class for domain value objects."""

{% set base_class = cookiecutter.base_classes.value_object_base.split('.') %}
{% if base_class|length > 1 %}
from {{ '.'.join(base_class[:-1]) }} import {{ base_class[-1] }}
{% endif %}


class BaseValueObject({{ base_class[-1] }}):
    """Base class for all domain value objects."""

    def __eq__(self, other: object) -> bool:
        """Compare value objects by their values."""
        if not isinstance(other, BaseValueObject):
            return NotImplemented
        return self.model_dump() == other.model_dump()

    def __hash__(self) -> int:
        """Hash value object based on its values."""
        return hash(tuple(sorted(self.model_dump().items())))
