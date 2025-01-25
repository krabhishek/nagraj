from datetime import datetime, timezone
from uuid import UUID

import pytest
from {{cookiecutter.project_slug}}.common.bounded_contexts.auth.domain.aggregates.user_aggregate import (
    UserAggregate,
)
from {{cookiecutter.project_slug}}.common.bounded_contexts.auth.domain.events.user_events import (
    PasswordChangedEvent,
    UserActivatedEvent,
    UserCreatedEvent,
    UserDeactivatedEvent,
)


@pytest.fixture
def valid_user_data():
    """Fixture for valid user data."""
    return {
        "email": "test@example.com",
        "password": "Test@123456",  # Valid password with all requirements
    }


@pytest.fixture
def user_aggregate(valid_user_data):
    """Fixture for a valid user aggregate."""
    return UserAggregate.create(**valid_user_data)


def test_create_user_with_valid_data(valid_user_data):
    """Test creating a user with valid data."""
    user = UserAggregate.create(**valid_user_data)

    assert isinstance(user.id, UUID)
    assert user.email.value == valid_user_data["email"]
    assert user.is_active is True
    assert user.verify_password(valid_user_data["password"]) is True
    assert isinstance(user.created_at, datetime)
    assert isinstance(user.updated_at, datetime)
    assert len(user.domain_events) == 1
    assert isinstance(user.domain_events[0], UserCreatedEvent)


def test_create_user_with_invalid_email():
    """Test creating a user with an invalid email."""
    with pytest.raises(ValueError, match="value is not a valid email address"):
        UserAggregate.create(email="invalid-email", password="Test@123456")


def test_create_user_with_invalid_password():
    """Test creating a user with an invalid password."""
    with pytest.raises(ValueError, match="Password must be at least 8 characters"):
        UserAggregate.create(email="test@example.com", password="short")


def test_verify_password_with_correct_password(user_aggregate):
    """Test verifying a password with correct password."""
    assert user_aggregate.verify_password("Test@123456") is True


def test_verify_password_with_incorrect_password(user_aggregate):
    """Test verifying a password with incorrect password."""
    assert user_aggregate.verify_password("wrongpassword") is False


def test_change_password(user_aggregate):
    """Test changing a user's password."""
    new_password = "NewTest@123456"
    user_aggregate.change_password("Test@123456", new_password)

    assert user_aggregate.verify_password("Test@123456") is False
    assert user_aggregate.verify_password(new_password) is True
    assert len(user_aggregate.domain_events) == 2  # Created + Password Changed
    assert isinstance(user_aggregate.domain_events[-1], PasswordChangedEvent)


def test_change_password_with_incorrect_current_password(user_aggregate):
    """Test changing a password with incorrect current password."""
    with pytest.raises(ValueError, match="Current password is incorrect"):
        user_aggregate.change_password("wrongpassword", "NewTest@123456")


def test_change_password_with_invalid_new_password(user_aggregate):
    """Test changing a password to an invalid one."""
    with pytest.raises(ValueError, match="Password must be at least 8 characters"):
        user_aggregate.change_password("Test@123456", "short")


def test_deactivate_user(user_aggregate):
    """Test deactivating a user."""
    user_aggregate.deactivate()

    assert user_aggregate.is_active is False
    events = user_aggregate.domain_events
    assert len(events) == 2  # Created + Deactivated
    assert isinstance(events[-1], UserDeactivatedEvent)


def test_deactivate_already_inactive_user(user_aggregate):
    """Test deactivating an already inactive user."""
    user_aggregate.deactivate()
    with pytest.raises(ValueError, match="User is already inactive"):
        user_aggregate.deactivate()


def test_activate_user(user_aggregate):
    """Test activating a user."""
    user_aggregate.deactivate()
    user_aggregate.activate()

    assert user_aggregate.is_active is True
    events = user_aggregate.domain_events
    assert len(events) == 3  # Created + Deactivated + Activated
    assert isinstance(events[-1], UserActivatedEvent)


def test_activate_already_active_user(user_aggregate):
    """Test activating an already active user."""
    with pytest.raises(ValueError, match="User is already active"):
        user_aggregate.activate()


def test_update_last_login(user_aggregate):
    """Test updating last login timestamp."""
    now = datetime.now(timezone.utc)
    user_aggregate.update_last_login(now)
    assert user_aggregate.last_login == now
