class ApplicationException(Exception):
    """
    Base class for all application exceptions
    """

    def __init__(self, message: str, status_code: int = 500) -> None:
        super().__init__(message, status_code)


class InvalidRequestException(ApplicationException):
    """
    Exception raised when an invalid request is made
    """

    def __init__(self, message: str, status_code: int = 400) -> None:
        super().__init__(message, status_code)
