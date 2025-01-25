"""env file for alembic migrations."""

import asyncio
from logging.config import fileConfig

import sqlalchemy
from alembic import context
from nagraj_project_template.example_domain.bounded_contexts.example_context_two.infrastructure.orms.example_context_two_orm import (
    ExampleContextTwoORM,  # noqa: F401
)
from nagraj_project_template.example_domain.core.config.settings import settings
from nagraj_project_template.example_domain.core.logging import LoggerService
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel

logger = LoggerService().get_logger({"module": "migrations"})
# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def get_url():
    return (
        f"postgresql+asyncpg://{settings.db_user}:{settings.db_password}"
        f"@{settings.db_host}:{settings.db_port}/{settings.db_name}"
    )


async def initialize_schemas():
    if settings.db_schemas is not None:
        logger.info(f"Initializing schemas: {settings.db_schemas}")
        engine = create_async_engine(get_url())
        async with engine.begin() as conn:
            for schema in settings.db_schemas:
                statement = sqlalchemy.text(f"CREATE SCHEMA IF NOT EXISTS {schema}")
                await conn.run_sync(lambda conn: conn.execute(statement))


def get_target_metadata():
    """Import all models here to register them with SQLModel.metadata"""
    # Auth models

    # Add other bounded contexts' models here

    return SQLModel.metadata


target_metadata = get_target_metadata()


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        version_table_schema="auth",  # Keep version table in auth schema
        include_schemas=True,  # Enable schema support
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = create_async_engine(get_url())

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    asyncio.run(initialize_schemas())
    run_migrations_offline()
else:
    asyncio.run(initialize_schemas())
    asyncio.run(run_migrations_online())
