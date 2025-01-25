from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from {{ cookiecutter.project_slug }}.common.bounded_contexts.auth.interfaces.apis.routes.v1.auth import (
    router as auth_router,
)
from {{ cookiecutter.project_slug }}.common.core.infrastructure.database.database import db
from {{ cookiecutter.project_slug }}.common.core.logging.api_logs import (
    setup_logging_middleware,
)



@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for database connection."""
    # Startup
    await db.create_pool()
    yield
    # Shutdown
    await db.close_pool()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Auth Service",
        description="Authentication service with DDD and CQRS patterns",
        version="1.0.0",
        lifespan=lifespan,
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, replace with specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add logging middleware
    setup_logging_middleware(app)

    # Include routers
    app.include_router(auth_router, prefix="/api/v1/auth")
 
    return app
