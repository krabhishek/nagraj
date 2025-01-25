from pathlib import Path

from {{cookiecutter.project_slug}}.common.base.domain_event import BaseDomainEvent
from {{cookiecutter.project_slug}}.common.base.event_handler import BaseEventHandler
from {{cookiecutter.project_slug}}.common.core.logging import LoggerService


class AuthEventHandler(BaseEventHandler):
    """Handler for auth domain events."""

    def __init__(self, log_file_path: str = "logs/auth_events.log"):
        self.logger = LoggerService().get_logger({"module": "auth_events"})
        self.log_file_path = Path(log_file_path)
        self._ensure_log_directory()

    def _ensure_log_directory(self) -> None:
        """Ensure the log directory exists."""
        self.log_file_path.parent.mkdir(parents=True, exist_ok=True)

    async def handle(self, event: BaseDomainEvent) -> None:
        """Handle an auth domain event."""
        # Log to file
        try:
            with open(self.log_file_path, "a", encoding="utf-8") as f:
                f.write(event.model_dump_json())
                f.write("\n")
        except Exception as e:
            self.logger.error(f"Failed to write event to log file: {str(e)}")

        # Log through service
        self.logger.info(
            f"Domain event occurred: {event.event_type}",
            extra={"event_data": event.model_dump()},
        )
