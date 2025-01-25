"""
Exceptions
"""

from .application_exceptions import InvalidRequestException
from .domain_exceptions import (
    DomainException,
    EntityAlreadyExistsException,
    EntityNotFoundException,
)
from .infrastructure_exceptions import (
    DatabaseException,
    InfrastructureException,
    RepositoryException,
)

__all__ = [
    # Domain exceptions
    "DomainException",
    "EntityAlreadyExistsException",
    "EntityNotFoundException",
    # Application exceptions
    "InvalidRequestException",
    # Infrastructure exceptions
    "DatabaseException",
    "InfrastructureException",
    "RepositoryException",
]
