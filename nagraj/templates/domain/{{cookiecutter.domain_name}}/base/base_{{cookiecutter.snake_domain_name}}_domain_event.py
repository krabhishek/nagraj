"""Base domain event for {{ cookiecutter.domain_name }} domain."""

from src.shared.base.base_domain_event import BaseDomainEvent


class Base{{ cookiecutter.pascal_domain_name }}DomainEvent(BaseDomainEvent):
    """Base domain event class for {{ cookiecutter.domain_name }} domain.
    
    All domain events in this domain should inherit from this class.
    """
    pass 