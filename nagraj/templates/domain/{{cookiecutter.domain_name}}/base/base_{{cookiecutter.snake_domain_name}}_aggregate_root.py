"""Base aggregate root for {{ cookiecutter.domain_name }} domain."""

from src.shared.base.base_aggregate_root import BaseAggregateRoot


class Base{{ cookiecutter.pascal_domain_name }}AggregateRoot(BaseAggregateRoot):
    """Base aggregate root class for {{ cookiecutter.domain_name }} domain.
    
    All aggregate roots in this domain should inherit from this class.
    """
    pass 