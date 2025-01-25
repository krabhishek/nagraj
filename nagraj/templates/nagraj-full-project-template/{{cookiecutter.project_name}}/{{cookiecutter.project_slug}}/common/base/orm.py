from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import TIMESTAMP, Integer
from sqlmodel import Field, SQLModel


class BaseORM(SQLModel):
    """
    Base ORM class
    """

    id: UUID = Field(default_factory=lambda: uuid4(), primary_key=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=TIMESTAMP(timezone=True),  # type: ignore
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=TIMESTAMP(timezone=True),  # type: ignore
    )

    version: int = Field(
        default=1,
        sa_type=Integer,
        nullable=False,
        index=True,
    )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.id}>"

    def __str__(self) -> str:
        return f"{self.__class__.__name__} {self.id}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseORM):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
