"""User adapter for converting between domain and persistence models."""

from ...domain.aggregates.user_aggregate import UserAggregate
from ...domain.value_objects.email import Email
from ...domain.value_objects.password import Password
from ..orms.user_orm import UserORM


class UserAdapter:
    """Adapter for converting between User domain and ORM models."""

    @staticmethod
    def to_orm(aggregate: UserAggregate) -> UserORM:
        """Convert a user aggregate to ORM model."""
        return UserORM(
            id=aggregate.id,
            email=str(aggregate.email),
            password_hash=aggregate.password.hashed_value,
            is_active=aggregate.is_active,
            last_login=aggregate.last_login,
            created_at=aggregate.created_at,
            updated_at=aggregate.updated_at,
        )

    @staticmethod
    def to_aggregate(orm: UserORM) -> UserAggregate:
        """Convert an ORM model to user aggregate."""
        return UserAggregate(
            id=orm.id,
            email=Email.create(orm.email),
            password=Password.from_hash(orm.password_hash),
            is_active=orm.is_active,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
            domain_events=[],
        )
