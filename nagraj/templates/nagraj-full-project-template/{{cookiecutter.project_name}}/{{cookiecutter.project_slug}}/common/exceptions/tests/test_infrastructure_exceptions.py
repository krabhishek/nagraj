"""Tests for infrastructure exceptions."""

from ..infrastructure_exceptions import (
    DatabaseException,
    DeleteOperationFailedException,
    EntityNotFoundRepositoryException,
    ExternalServiceException,
    InfrastructureException,
    RepositoryException,
    SaveOperationFailedException,
    UpdateOperationFailedException,
)


def test_infrastructure_exception_with_default_status():
    """Test InfrastructureException with default status code."""
    exception = InfrastructureException("Test error message")
    assert str(exception) == "('Test error message', 500)"


def test_infrastructure_exception_with_custom_status():
    """Test InfrastructureException with custom status code."""
    exception = InfrastructureException("Test error message", status_code=400)
    assert str(exception) == "('Test error message', 400)"


def test_database_exception():
    """Test DatabaseException."""
    exception = DatabaseException("Database connection failed")
    assert str(exception) == "('Database connection failed', 500)"
    assert isinstance(exception, InfrastructureException)


def test_external_service_exception():
    """Test ExternalServiceException."""
    exception = ExternalServiceException("External API error")
    assert str(exception) == "('External API error', 500)"
    assert isinstance(exception, InfrastructureException)


def test_repository_exception():
    """Test RepositoryException."""
    exception = RepositoryException("Repository operation failed")
    assert str(exception) == "('Repository operation failed', 500)"
    assert isinstance(exception, InfrastructureException)


def test_entity_not_found_repository_exception():
    """Test EntityNotFoundRepositoryException."""
    exception = EntityNotFoundRepositoryException("User not found")
    assert str(exception) == "('User not found', 404)"
    assert isinstance(exception, RepositoryException)


def test_save_operation_failed_exception():
    """Test SaveOperationFailedException."""
    exception = SaveOperationFailedException("Failed to save user")
    assert str(exception) == "('Failed to save user', 500)"
    assert isinstance(exception, RepositoryException)


def test_delete_operation_failed_exception():
    """Test DeleteOperationFailedException."""
    exception = DeleteOperationFailedException("Failed to delete user")
    assert str(exception) == "('Failed to delete user', 500)"
    assert isinstance(exception, RepositoryException)


def test_update_operation_failed_exception():
    """Test UpdateOperationFailedException."""
    exception = UpdateOperationFailedException("Failed to update user")
    assert str(exception) == "('Failed to update user', 500)"
    assert isinstance(exception, RepositoryException)


def test_exception_inheritance_chain():
    """Test the complete inheritance chain of repository exceptions."""
    exceptions = [
        EntityNotFoundRepositoryException("Not found"),
        SaveOperationFailedException("Save failed"),
        DeleteOperationFailedException("Delete failed"),
        UpdateOperationFailedException("Update failed"),
    ]

    for exception in exceptions:
        assert isinstance(exception, RepositoryException)
        assert isinstance(exception, InfrastructureException)
        assert isinstance(exception, Exception)
