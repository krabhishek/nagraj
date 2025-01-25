"""Unit tests for the logger service."""

from unittest.mock import patch

from nagraj.core.logging import LoggerService, logger_service


def test_logger_service_singleton():
    """Test that LoggerService follows singleton pattern."""
    logger1 = LoggerService()
    logger2 = LoggerService()
    assert logger1 is logger2


def test_logger_service_global_instance():
    """Test that global logger_service instance is a LoggerService."""
    assert isinstance(logger_service, LoggerService)
    assert logger_service is LoggerService()


def test_logger_service_initialization():
    """Test logger service initialization."""
    with patch("nagraj.core.logging.logger") as mock_logger:
        # Create a new instance to trigger configuration
        LoggerService._instance = None
        LoggerService()
        
        # Verify logger configuration
        mock_logger.remove.assert_called_once()
        assert mock_logger.level.call_count == 6  # All log levels
        mock_logger.add.assert_called_once()
        mock_logger.configure.assert_called_once()
        
        # Verify default configuration
        configure_kwargs = mock_logger.configure.call_args[1]
        assert configure_kwargs["extra"] == {"app_name": "{{ cookiecutter.project_slug }}"}


def test_get_logger_without_context():
    """Test getting logger without context."""
    with patch("nagraj.core.logging.logger") as mock_logger:
        logger = logger_service.get_logger()
        assert logger is not None
        assert logger == mock_logger


def test_get_logger_with_context():
    """Test getting logger with context."""
    with patch("nagraj.core.logging.logger") as mock_logger:
        context = {"request_id": "123", "user_id": "456"}
        logger = logger_service.get_logger(context)
        assert logger is not None
        # Verify that bind was called with the correct context
        mock_logger.bind.assert_called_once_with(**context)


def test_get_contextualized_logger():
    """Test getting contextualized logger."""
    with patch("nagraj.core.logging.logger") as mock_logger:
        logger = logger_service.get_contextualized_logger(
            request_id="123",
            user_id="456"
        )
        assert logger is not None
        # Verify that bind was called with the correct kwargs
        mock_logger.bind.assert_called_once_with(request_id="123", user_id="456") 