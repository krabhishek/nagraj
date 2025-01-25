import os
import sys
from typing import Any, Dict

from loguru import logger


class LoggerService:
    """
    A service class that configures and provides logging functionality using Loguru.
    Implements a singleton pattern to ensure consistent logging configuration across the application.
    """

    _instance = None

    def __new__(cls) -> "LoggerService":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._configure_logger()
        return cls._instance

    def _configure_logger(self) -> None:
        """Configure the logger with application-specific settings"""
        # Remove default logger
        logger.remove()
        logger.level("INFO", icon="🟢", color="<white>")
        logger.level("ERROR", icon="❌", color="<red>")
        logger.level("WARNING", icon="⚠️  ", color="<yellow>")
        logger.level("DEBUG", icon="🔍", color="<blue>")
        logger.level("CRITICAL", icon="🔴", color="<red>")
        logger.level("SUCCESS", icon="✅", color="<green>")
        # Add console handler with custom format
        logger.add(
            sys.stderr,
            level=os.environ.get("LOG_LEVEL", "INFO"),
            format=(
                "<green>{time:HH:mm:ss.SSS}</green> | "
                "<level>{level.icon: <2} {level: <8}</level> | "
                "<level>{name}</level>:<level>{function}</level>:<level>{line}</level> | "
                "<level>{message}</level> <r><b>//</b> </r>"
                "<white>{extra}</white>"
            ),
            colorize=True,
            enqueue=True,
        )

        # Configure default extra fields
        logger.configure(extra={"app_name": "{{ cookiecutter.project_slug }}"})

    def get_logger(self, context: Dict[str, Any] | None = None): # type: ignore[no-untyped-def]
        """
        Get a contextualized logger instance.

        Args:
            context: Optional dictionary of context variables to bind to the logger

        Returns:
            A configured logger instance with bound context
        """
        if context:
            return logger.bind(**context)
        return logger

    def get_contextualized_logger(self, **kwargs: Any): # type: ignore[no-untyped-def]
        """
        Get a logger with context variables bound to it.

        Args:
            **kwargs: Arbitrary keyword arguments to bind as context

        Returns:
            A logger instance with bound context
        """
        return logger.bind(**kwargs)


# Create a global logger service instance
logger_service = LoggerService()
