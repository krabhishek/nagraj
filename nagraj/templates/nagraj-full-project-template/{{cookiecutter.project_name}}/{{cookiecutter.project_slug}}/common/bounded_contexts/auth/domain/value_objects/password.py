from typing import Any, ClassVar

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from .....base.specification import BaseSpecification
from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema


class Password:
    """Value object representing a password."""

    # Class-level PasswordHasher instance for reuse
    _ph: ClassVar[PasswordHasher] = PasswordHasher()

    def __init__(
        self,
        value: str,
        hashed: bool = False,
        validator: BaseSpecification[str] | None = None,
    ):
        """Initialize password."""
        if not hashed and validator and not validator.is_satisfied_by(value):
            raise ValueError("Password must be at least 8 characters")
        self._hashed_value = value if hashed else self._ph.hash(value)

    @classmethod
    def from_hash(cls, hashed_value: str) -> "Password":
        """Create a Password object from a hashed value."""
        return cls(hashed_value, hashed=True)

    @property
    def hashed_value(self) -> str:
        """Get the hashed value."""
        return self._hashed_value

    def verify(self, plain_password: str) -> bool:
        """Verify if the plain password matches the hashed one."""
        try:
            return self._ph.verify(self._hashed_value, plain_password)
        except VerifyMismatchError:
            return False

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Password):
            return NotImplemented
        return self._hashed_value == other._hashed_value

    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Any, _handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        """Define how Pydantic should handle this type."""
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema(
                [
                    # Handle direct Password instances
                    core_schema.is_instance_schema(cls),
                    # Handle string inputs by creating new Password
                    core_schema.no_info_plain_validator_function(
                        lambda x: cls(x) if isinstance(x, str) else x
                    ),
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: x.hashed_value if isinstance(x, Password) else x
            ),
        )
