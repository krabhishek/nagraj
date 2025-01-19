"""{{ cookiecutter.description or 'Entity representing ' + cookiecutter.pascal_entity_name }}."""

from typing import Optional

from pydantic import Field

from src.shared.base.base_entity import BaseEntity


class {{ cookiecutter.pascal_entity_name }}(BaseEntity):
    """{{ cookiecutter.description or 'Entity representing ' + cookiecutter.pascal_entity_name }}.

    Attributes:
        id: The unique identifier of the {{ cookiecutter.entity_name }}.
    """

    id: str = Field(description="The unique identifier of the {{ cookiecutter.entity_name }}")
    # Add your entity attributes here 