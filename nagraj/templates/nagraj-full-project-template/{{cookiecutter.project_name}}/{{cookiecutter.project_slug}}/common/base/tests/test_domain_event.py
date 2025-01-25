"""Tests for BaseDomainEvent class."""

from datetime import datetime, timezone
from uuid import UUID, uuid4

import pytest

from {{ cookiecutter.project_slug }}.common.base.domain_event import BaseDomainEvent


class TestDomainEvent(BaseDomainEvent):
    """Test domain event class."""

    test_data: str = "test"


@pytest.fixture
def event_id():
    """Fixture for event ID."""
    return uuid4()


@pytest.fixture
def aggregate_id():
    """Fixture for aggregate ID."""
    return uuid4()


@pytest.fixture
def occurred_on():
    """Fixture for event timestamp."""
    return datetime.now(timezone.utc)


def test_domain_event_creation(event_id, aggregate_id, occurred_on):
    """Test creating a domain event with default values."""
    event = TestDomainEvent(
        event_id=event_id,
        aggregate_id=aggregate_id,
        occurred_on=occurred_on,
    )

    assert isinstance(event.event_id, UUID)
    assert isinstance(event.aggregate_id, UUID)
    assert isinstance(event.occurred_on, datetime)
    assert event.event_type == "TestDomainEvent"
    assert event.event_version == 1
    assert event.test_data == "test"


def test_domain_event_with_custom_values(event_id, aggregate_id, occurred_on):
    """Test creating a domain event with custom values."""
    event = TestDomainEvent(
        event_id=event_id,
        aggregate_id=aggregate_id,
        occurred_on=occurred_on,
        event_type="custom_event",
        event_version=2,
        test_data="custom",
    )

    assert event.event_type == "custom_event"
    assert event.event_version == 2
    assert event.test_data == "custom"


def test_domain_event_equality(event_id, aggregate_id, occurred_on):
    """Test domain event equality comparison."""
    event1 = TestDomainEvent(
        event_id=event_id,
        aggregate_id=aggregate_id,
        occurred_on=occurred_on,
    )
    event2 = TestDomainEvent(
        event_id=event_id,
        aggregate_id=aggregate_id,
        occurred_on=occurred_on,
    )
    event3 = TestDomainEvent(
        event_id=uuid4(),
        aggregate_id=aggregate_id,
        occurred_on=occurred_on,
    )

    assert event1 == event2
    assert event1 != event3


def test_domain_event_hash(event_id, aggregate_id, occurred_on):
    """Test domain event hash."""
    event1 = TestDomainEvent(
        event_id=event_id,
        aggregate_id=aggregate_id,
        occurred_on=occurred_on,
    )
    event2 = TestDomainEvent(
        event_id=event_id,
        aggregate_id=aggregate_id,
        occurred_on=occurred_on,
    )

    assert hash(event1) == hash(event2)


def test_domain_event_repr(event_id, aggregate_id, occurred_on):
    """Test domain event string representation."""
    event = TestDomainEvent(
        event_id=event_id,
        aggregate_id=aggregate_id,
        occurred_on=occurred_on,
    )

    repr_str = repr(event)
    assert "TestDomainEvent" in repr_str
    assert str(event_id) in repr_str
    assert "event_type" in repr_str


def test_domain_event_json_serialization(event_id, aggregate_id, occurred_on):
    """Test domain event JSON serialization."""
    event = TestDomainEvent(
        event_id=event_id,
        aggregate_id=aggregate_id,
        occurred_on=occurred_on,
    )

    json_str = event.model_dump_json()
    assert isinstance(json_str, str)
    assert str(event_id) in json_str


def test_domain_event_validation_error():
    """Test validation error handling."""
    # Test with invalid datetime format
    with pytest.raises(
        ValueError, match="occurred_on must be a valid ISO format datetime"
    ):
        TestDomainEvent(
            event_id=uuid4(),
            aggregate_id=uuid4(),
            occurred_on="not a datetime",  # type: ignore
            test_data="test",
        )

    naive_datetime = datetime(2024, 1, 1)
    with pytest.raises(ValueError, match="Datetime must be timezone-aware"):
        TestDomainEvent(
            event_id=uuid4(),
            aggregate_id=uuid4(),
            occurred_on=naive_datetime,
            test_data="test",
        )


def test_domain_event_json_deserialization_error():
    """Test error handling in JSON deserialization."""
    # Test with invalid JSON format
    invalid_json = '{"test_data": "test", "event_id": "not-a-uuid"}'
    with pytest.raises(ValueError, match="Failed to deserialize domain event"):
        TestDomainEvent.from_json(invalid_json)

    # Test with invalid datetime format
    invalid_datetime_json = '{"event_id": "123e4567-e89b-12d3-a456-426614174000", "occurred_on": "invalid-datetime", "event_type": "TestDomainEvent", "event_version": 1, "test_data": "test"}'
    with pytest.raises(ValueError, match="Failed to deserialize domain event"):
        TestDomainEvent.from_json(invalid_datetime_json)
