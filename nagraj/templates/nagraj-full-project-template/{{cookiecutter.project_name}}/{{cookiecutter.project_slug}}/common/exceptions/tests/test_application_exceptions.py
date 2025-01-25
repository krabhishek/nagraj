"""Tests for application exceptions."""

from ..application_exceptions import (
    ApplicationException,
    InvalidRequestException,
)


def test_application_exception_with_default_status():
    """Test ApplicationException with default status code."""
    exception = ApplicationException("Test error message")
    assert str(exception) == "('Test error message', 500)"


def test_application_exception_with_custom_status():
    """Test ApplicationException with custom status code."""
    exception = ApplicationException("Test error message", status_code=400)
    assert str(exception) == "('Test error message', 400)"


def test_invalid_request_exception_with_default_status():
    """Test InvalidRequestException with default status code."""
    exception = InvalidRequestException("Invalid request")
    assert str(exception) == "('Invalid request', 400)"


def test_invalid_request_exception_with_custom_status():
    """Test InvalidRequestException with custom status code."""
    exception = InvalidRequestException("Invalid request", status_code=422)
    assert str(exception) == "('Invalid request', 422)"


def test_exception_inheritance():
    """Test inheritance relationships of application exceptions."""
    exception = InvalidRequestException("Invalid request")
    assert isinstance(exception, ApplicationException)
    assert isinstance(exception, Exception)
