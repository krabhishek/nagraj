class InfrastructureException(Exception):
    """
    Base class for all infrastructure exceptions
    """

    def __init__(self, message: str, status_code: int = 500) -> None:
        from ..core.logging import LoggerService

        logger = LoggerService().get_logger({"module": "infrastructure_exceptions"})
        logger.debug(f"InfrastructureException: {message}, status_code: {status_code}")
        super().__init__(message, status_code)


class DatabaseException(InfrastructureException):
    """
    Exception raised when a database error occurs
    """

    def __init__(self, message: str, status_code: int = 500) -> None:
        super().__init__(message, status_code)


class ExternalServiceException(InfrastructureException):
    """
    Exception raised when an external service error occurs
    """

    def __init__(self, message: str, status_code: int = 500) -> None:
        super().__init__(message, status_code)


class RepositoryException(InfrastructureException):
    """
    Exception raised when a repository error occurs
    """

    def __init__(self, message: str, status_code: int = 500) -> None:
        super().__init__(message, status_code)


class EntityNotFoundRepositoryException(RepositoryException):
    """
    Exception raised when an entity is not found in the repository
    """

    def __init__(self, message: str, status_code: int = 404) -> None:
        super().__init__(message, status_code)


class SaveOperationFailedException(RepositoryException):
    """
    Exception raised when a save operation fails
    """

    def __init__(self, message: str, status_code: int = 500) -> None:
        super().__init__(message, status_code)


class DeleteOperationFailedException(RepositoryException):
    """
    Exception raised when a delete operation fails
    """

    def __init__(self, message: str, status_code: int = 500) -> None:
        super().__init__(message, status_code)


class UpdateOperationFailedException(RepositoryException):
    """
    Exception raised when an update operation fails
    """

    def __init__(self, message: str, status_code: int = 500) -> None:
        super().__init__(message, status_code)
