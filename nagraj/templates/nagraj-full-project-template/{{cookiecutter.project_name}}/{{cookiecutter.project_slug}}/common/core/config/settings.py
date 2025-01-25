import os

from dotenv import load_dotenv
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE_NAME = os.getenv("DOMAIN_ENV_FILE", ".env")

load_dotenv(ENV_FILE_NAME)


class DomainSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE_NAME,
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        validate_assignment=True,
        extra="allow",
    )

    db_host: str = Field(
        alias="DB_HOST",
        default_factory=lambda: os.getenv("DB_HOST", ""),
    )

    @field_validator("db_host", mode="before")
    @classmethod
    def validate_db_host(cls, value: str | None) -> str:
        if value is None or value == "":
            raise ValueError("DB_HOST is required")
        return value

    db_port: int = Field(
        alias="DB_PORT",
        default_factory=lambda: int(os.getenv("DB_PORT", 0)),
    )

    @field_validator("db_port", mode="before")
    @classmethod
    def validate_db_port(cls, value: int) -> int:
        if value is None or value == 0:
            raise ValueError("DB_PORT is required")
        return value

    db_user: str = Field(
        alias="DB_USER",
        default_factory=lambda: os.getenv("DB_USER", ""),
    )

    @field_validator("db_user", mode="before")
    @classmethod
    def validate_db_user(cls, value: str | None) -> str:
        if value is None or value == "":
            raise ValueError("DB_USER is required")
        return value

    db_password: str = Field(
        alias="DB_PASSWORD",
        default_factory=lambda: os.getenv("DB_PASSWORD", ""),
    )

    @field_validator("db_password", mode="before")
    @classmethod
    def validate_db_password(cls, value: str | None) -> str:
        if value is None or value == "":
            raise ValueError("DB_PASSWORD is required")
        return value

    db_name: str = Field(
        alias="DB_NAME",
        default_factory=lambda: os.getenv("DB_NAME", ""),
    )

    @field_validator("db_name", mode="before")
    @classmethod
    def validate_db_name(cls, value: str | None) -> str:
        if value is None or value == "":
            raise ValueError("DB_NAME is required")
        return value

    db_schemas_str: str = Field(alias="DB_SCHEMAS", default="public,auth")

    @property
    def db_schemas(self) -> list[str]:
        """Get the list of database schemas."""
        if not self.db_schemas_str:
            return ["public", "auth"]
        return [
            schema.strip()
            for schema in self.db_schemas_str.split(",")
            if schema.strip()
        ]

    @field_validator("db_schemas_str")
    @classmethod
    def validate_db_schemas(cls, value: str | None) -> str:
        if value is None or not value.strip():
            return "public,auth"
        return value.strip()

    jwt_secret_key: str = Field(
        alias="JWT_SECRET_KEY",
        default_factory=lambda: os.getenv("JWT_SECRET_KEY", ""),
    )

    @field_validator("jwt_secret_key", mode="before")
    @classmethod
    def validate_jwt_secret_key(cls, value: str | None) -> str:
        if value is None or value == "":
            raise ValueError("JWT_SECRET_KEY is required")
        return value

    jwt_algorithm: str = Field(
        alias="JWT_ALGORITHM",
        default_factory=lambda: os.getenv("JWT_ALGORITHM", "HS256"),
    )

    jwt_access_token_expire_minutes: int = Field(
        alias="JWT_ACCESS_TOKEN_EXPIRE_MINUTES",
        default_factory=lambda: int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "60")),
    )

    log_level: str = Field(
        alias="LOG_LEVEL",
        default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"),
    )

    log_to_file: bool = Field(
        alias="LOG_TO_FILE",
        default_factory=lambda: os.getenv("LOG_TO_FILE", "false").lower() == "true",
    )


settings = DomainSettings()
