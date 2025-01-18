"""Base value object for {{ cookiecutter.domain_name }} domain."""

from src.shared.base.base_value_object import BaseValueObject


class Base{{ cookiecutter.pascal_domain_name }}ValueObject(BaseValueObject):
    """Base value object class for {{ cookiecutter.domain_name }} domain.
    
    All value objects in this domain should inherit from this class.
    """
    pass 