from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

import asyncpg
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.pool import AsyncAdaptedQueuePool
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from ...config.settings import settings
from ....exceptions.infrastructure_exceptions import (
    DatabaseException,
)

from ...config.settings import DomainSettings
from ...logging import LoggerService

logger = LoggerService().get_logger({"module": "database"})


class Database:
    """Database connection manager."""

    def __init__(self):
        self._engine: Optional[AsyncEngine] = None
        self._pool: Optional[asyncpg.Pool] = None
        self._settings = DomainSettings()
        self.connection_url = (
            f"postgresql+asyncpg://{settings.db_user}:{settings.db_password}"
            f"@{settings.db_host}:{settings.db_port}/{settings.db_name}"
        )

    async def create_pool(self, schema: Optional[str] = None) -> None:
        """Create database connection pool."""
        try:
            logger.info("Creating database connection pool...", module="database")

            self._pool = await asyncpg.create_pool(
                host=self._settings.db_host,
                port=self._settings.db_port,
                user=self._settings.db_user,
                password=self._settings.db_password,
                database=self._settings.db_name,
            )

            if schema:
                # Create schema if it doesn't exist and set it as the default for this connection
                async with self._pool.acquire() as connection:
                    await connection.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
                    await connection.execute(f"SET search_path TO {schema}")
                logger.info(f"Created/set schema: {schema}", module="database")

        except Exception as e:
            logger.error(f"Failed to create database pool: {str(e)}", module="database")
            raise DatabaseException(f"Failed to create database pool: {str(e)}")

    @property
    def pool(self) -> asyncpg.Pool:
        """Get the connection pool."""
        if not self._pool:
            raise DatabaseException("Database pool not initialized")
        return self._pool

    async def close_pool(self) -> None:
        """Close the connection pool."""
        if self._pool:
            await self._pool.close()
            self._pool = None

    @property
    def engine(self) -> AsyncEngine:
        """Get the SQLAlchemy async engine."""
        if not self._engine:
            try:
                logger.info("Creating SQLAlchemy engine...")
                self._engine = create_async_engine(
                    self.connection_url,
                    echo=False,
                    future=True,
                    poolclass=AsyncAdaptedQueuePool,
                    pool_pre_ping=True,
                    pool_size=20,
                    max_overflow=10,
                )
                logger.info("SQLAlchemy engine created successfully")
            except Exception as e:
                logger.error(f"Failed to create SQLAlchemy engine: {str(e)}")
                raise DatabaseException(f"Failed to create SQLAlchemy engine: {str(e)}")
        return self._engine

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get a database session."""
        session = AsyncSession(self.engine, expire_on_commit=False)
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {str(e)}")
            await session.rollback()
            raise DatabaseException(f"Database session error: {str(e)}")
        finally:
            await session.close()

    @asynccontextmanager
    async def connection(self) -> AsyncGenerator[asyncpg.Connection, None]:
        """Get a raw database connection from the pool."""
        if not self._pool:
            await self.create_pool()

        pool = self._pool
        if not pool:
            raise DatabaseException("Database pool is not initialized")

        conn = await pool.acquire()
        try:
            yield conn
        except Exception as e:
            logger.error(f"Database connection error: {str(e)}")
            raise DatabaseException(f"Database connection error: {str(e)}")
        finally:
            await pool.release(conn)

    async def create_database(self) -> None:
        """Create all database tables."""
        try:
            logger.info("Creating database tables...")
            async with self.engine.begin() as conn:
                await conn.run_sync(SQLModel.metadata.create_all)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to create database tables: {str(e)}")
            raise DatabaseException(f"Failed to create database tables: {str(e)}")


# Global database instance
db = Database()
