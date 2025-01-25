"""File-based event store implementation."""

import json
from pathlib import Path
from typing import List
from uuid import UUID

from {{cookiecutter.project_slug}}.common.base.domain_event import BaseDomainEvent
from {{cookiecutter.project_slug}}.common.base.event_store import BaseEventStore
from {{cookiecutter.project_slug}}.common.core.logging import LoggerService


class FileEventStore(BaseEventStore):
    """File-based event store implementation."""

    def __init__(self, log_dir: str = "logs/events"):
        self._log_dir = Path(log_dir)
        self._logger = LoggerService().get_logger({"module": "file_event_store"})
        self._ensure_log_directory()

    def _ensure_log_directory(self) -> None:
        """Ensure the log directory exists."""
        self._log_dir.mkdir(parents=True, exist_ok=True)

    def _get_event_file(self, aggregate_id: UUID) -> Path:
        """Get the event file path for an aggregate."""
        return self._log_dir / f"{aggregate_id}.json"

    async def append_events(self, events: List[BaseDomainEvent]) -> None:
        """Append events to the store."""
        try:
            for event in events:
                event_file = self._get_event_file(event.aggregate_id)
                event_data = event.model_dump_json()

                with open(event_file, "a", encoding="utf-8") as f:
                    f.write(event_data + "\n")

                self._logger.info(
                    f"Event {event.event_type} stored for aggregate {event.aggregate_id}"
                )
        except Exception as e:
            self._logger.error(f"Failed to store events: {str(e)}")
            raise

    async def get_events(self, aggregate_id: UUID) -> List[BaseDomainEvent]:
        """Get all events for an aggregate."""
        event_file = self._get_event_file(aggregate_id)
        if not event_file.exists():
            return []

        events: List[BaseDomainEvent] = []
        try:
            with open(event_file, "r", encoding="utf-8") as f:
                for line in f:
                    event_data = json.loads(line.strip())
                    events.append(BaseDomainEvent.model_validate(event_data))
            return events
        except Exception as e:
            self._logger.error(f"Failed to read events: {str(e)}")
            raise

    async def get_events_since(
        self, aggregate_id: UUID, since_version: int
    ) -> List[BaseDomainEvent]:
        """Get events for an aggregate since a specific version."""
        all_events = await self.get_events(aggregate_id)
        return [event for event in all_events if event.event_version > since_version]
