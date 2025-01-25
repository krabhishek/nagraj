"""Tests for domain exceptions."""

from ..domain_exceptions import (
    DomainException,
    EntityAlreadyExistsException,
    EntityNotFoundException,
)


def test_domain_exception_with_default_status():
    """Test DomainException with default status code."""
    exception = DomainException("Test error message")
    assert exception.message == "Test error message"
    assert exception.status_code == 500
    assert str(exception) == "('Test error message', 500)"


def test_domain_exception_with_custom_status():
    """Test DomainException with custom status code."""
    exception = DomainException("Test error message", status_code=400)
    assert exception.message == "Test error message"
    assert exception.status_code == 400


def test_entity_not_found_exception_with_default_status():
    """Test EntityNotFoundException with default status code."""
    entity_id = "123"
    exception = EntityNotFoundException(entity_id)
    assert exception.message == f"Entity with id {entity_id} not found"
    assert exception.status_code == 404


def test_entity_not_found_exception_with_custom_status():
    """Test EntityNotFoundException with custom status code."""
    entity_id = "123"
    exception = EntityNotFoundException(entity_id, status_code=400)
    assert exception.message == f"Entity with id {entity_id} not found"
    assert exception.status_code == 400


def test_entity_already_exists_exception_with_default_status():
    """Test EntityAlreadyExistsException with default status code."""
    entity_id = "123"
    exception = EntityAlreadyExistsException(entity_id)
    assert exception.message == f"Entity with id {entity_id} already exists"
    assert exception.status_code == 400


def test_entity_already_exists_exception_with_custom_status():
    """Test EntityAlreadyExistsException with custom status code."""
    entity_id = "123"
    exception = EntityAlreadyExistsException(entity_id, status_code=409)
    assert exception.message == f"Entity with id {entity_id} already exists"
    assert exception.status_code == 409


def test_domain_exception_inheritance():
    """Test inheritance relationships of domain exceptions."""
    entity_id = "123"
    not_found = EntityNotFoundException(entity_id)
    already_exists = EntityAlreadyExistsException(entity_id)

    assert isinstance(not_found, DomainException)
    assert isinstance(already_exists, DomainException)
    assert isinstance(not_found, Exception)
    assert isinstance(already_exists, Exception)
