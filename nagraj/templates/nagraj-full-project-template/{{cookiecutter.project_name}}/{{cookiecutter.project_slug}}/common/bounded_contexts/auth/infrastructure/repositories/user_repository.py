"""User repository for persistence operations."""

from typing import Optional
from uuid import UUID

from {{cookiecutter.project_slug}}.common.base import BaseRepository
from {{cookiecutter.project_slug}}.common.core.infrastructure.database.database import db
from {{cookiecutter.project_slug}}.common.exceptions.infrastructure_exceptions import (
    DatabaseException,
)
from sqlmodel import select

from ...domain.aggregates.user_aggregate import UserAggregate
from ..adapters.user_adapter import UserAdapter
from ..orms.user_orm import UserORM


class UserRepository(BaseRepository[UserAggregate]):
    """Repository for user persistence operations."""

    def __init__(self):
        """Initialize the repository."""
        super().__init__(schema="auth")
        self._adapter = UserAdapter()

    async def save(self, aggregate: UserAggregate) -> None:
        """Save a user aggregate."""
        try:
            orm_model = self._adapter.to_orm(aggregate)
            async with db.session() as session:
                # Check if user exists
                statement = select(UserORM).where(UserORM.id == aggregate.id)
                result = await session.exec(statement)
                existing_user = result.first()

                if existing_user:
                    # Update existing user
                    existing_user.email = orm_model.email
                    existing_user.password_hash = orm_model.password_hash
                    existing_user.is_active = orm_model.is_active
                    existing_user.last_login = orm_model.last_login
                    existing_user.updated_at = orm_model.updated_at
                    # Increment version on update
                    existing_user.version += 1
                    session.add(existing_user)
                else:
                    # Insert new user (version starts at 1 from BaseORM)
                    session.add(orm_model)

                await session.commit()

                # Update aggregate version to match ORM
                aggregate.increment_version()
        except Exception as e:
            raise DatabaseException(f"Failed to save user: {str(e)}")

    async def get_by_id(self, id: UUID) -> Optional[UserAggregate]:
        """Get a user by ID."""
        try:
            async with db.session() as session:
                statement = select(UserORM).where(UserORM.id == id)
                result = await session.exec(statement)
                user_orm = result.first()
                if user_orm:
                    return self._adapter.to_aggregate(user_orm)
                return None
        except Exception as e:
            raise DatabaseException(f"Failed to get user by ID: {str(e)}")

    async def get_by_email(self, email: str) -> Optional[UserAggregate]:
        """Get a user by email."""
        try:
            async with db.session() as session:
                statement = select(UserORM).where(UserORM.email == email)
                result = await session.exec(statement)
                user_orm = result.first()
                if user_orm:
                    return self._adapter.to_aggregate(user_orm)
                return None
        except Exception as e:
            raise DatabaseException(f"Failed to get user by email: {str(e)}")

    async def delete(self, id: UUID) -> None:
        """Delete a user by ID."""
        try:
            async with db.session() as session:
                statement = select(UserORM).where(UserORM.id == id)
                result = await session.exec(statement)
                user_orm = result.first()
                if user_orm:
                    await session.delete(user_orm)
                    await session.commit()
        except Exception as e:
            raise DatabaseException(f"Failed to delete user: {str(e)}")

    async def check_version(self, id: UUID, expected_version: int) -> bool:
        """Check if the aggregate version matches the expected version."""
        try:
            async with db.session() as session:
                statement = select(UserORM).where(UserORM.id == id)
                result = await session.exec(statement)
                user_orm = result.first()
                return user_orm is not None and user_orm.version == expected_version
        except Exception as e:
            raise DatabaseException(f"Failed to check version: {str(e)}")
