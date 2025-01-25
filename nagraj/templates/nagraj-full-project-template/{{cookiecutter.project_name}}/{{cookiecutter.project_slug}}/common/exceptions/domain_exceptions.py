"""
Domain exceptions
"""

from typing import Optional


class DomainException(Exception):
    """
    Base class for all domain exceptions
    """

    def __init__(self, message: str, status_code: int = 500) -> None:
        from ..core.logging import LoggerService

        logger = LoggerService().get_logger({"module": "domain_exceptions"})
        self.message = message
        self.status_code = status_code
        logger.debug(f"DomainException: {message}, status_code: {status_code}")
        super().__init__(self.message, self.status_code)


class EntityNotFoundException(DomainException):
    """
    Exception raised when an entity is not found
    """

    def __init__(self, entity_id: str, status_code: Optional[int] = 404) -> None:
        message = f"Entity with id {entity_id} not found"
        status_code = status_code or 404
        super().__init__(message, status_code)


class EntityAlreadyExistsException(DomainException):
    """
    Exception raised when an entity already exists
    """

    def __init__(self, entity_id: str, status_code: Optional[int] = 400) -> None:
        message = f"Entity with id {entity_id} already exists"
        status_code = status_code or 400
        super().__init__(message, status_code)
