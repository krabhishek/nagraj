"""Base classes for {{ cookiecutter.domain_name }} domain."""

from .base_{{ cookiecutter.snake_domain_name }}_aggregate_root import Base{{ cookiecutter.pascal_domain_name }}AggregateRoot
from .base_{{ cookiecutter.snake_domain_name }}_domain_event import Base{{ cookiecutter.pascal_domain_name }}DomainEvent
from .base_{{ cookiecutter.snake_domain_name }}_entity import Base{{ cookiecutter.pascal_domain_name }}Entity
from .base_{{ cookiecutter.snake_domain_name }}_value_object import Base{{ cookiecutter.pascal_domain_name }}ValueObject

__all__ = [
    "Base{{ cookiecutter.pascal_domain_name }}AggregateRoot",
    "Base{{ cookiecutter.pascal_domain_name }}DomainEvent",
    "Base{{ cookiecutter.pascal_domain_name }}Entity",
    "Base{{ cookiecutter.pascal_domain_name }}ValueObject",
] 