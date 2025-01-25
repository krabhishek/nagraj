from datetime import datetime
from typing import Optional

from {{cookiecutter.project_slug}}.common.base import BaseORM
from sqlalchemy import TIMESTAMP
from sqlmodel import Field


class UserORM(BaseORM, table=True):
    """ORM model for user persistence."""

    __tablename__: str = "users"
    __table_args__: dict[str, str] = {"schema": "auth"}

    email: str = Field(
        unique=True,
        index=True,
        nullable=False,
    )
    password_hash: str = Field(nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    last_login: Optional[datetime] = Field(
        default=None,
        sa_type=TIMESTAMP(timezone=True),  # type: ignore
    )

    def __repr__(self) -> str:
        return f"UserORM(id={self.id}, email={self.email}, is_active={self.is_active})"
