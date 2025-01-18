"""Base entity for {{ cookiecutter.domain_name }} domain."""

from src.shared.base.base_entity import BaseEntity


class Base{{ cookiecutter.pascal_domain_name }}Entity(BaseEntity):
    """Base entity class for {{ cookiecutter.domain_name }} domain.
    
    All entities in this domain should inherit from this class.
    """
    pass 