import time

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from ..logging.logger import LoggerService

logger = LoggerService().get_logger({"module": "api"})


class APILoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging API requests and responses."""

    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """Process the request/response and log relevant information."""
        # Start timer
        start_time = time.time()

        # Prepare request logging
        method = request.method
        url = str(request.url)
        client_host = request.client.host if request.client else "unknown"

        # Log the incoming request
        logger.info(
            f"Incoming {method} request to {url}",
            extra={
                "client_host": client_host,
                "headers": dict(request.headers),
                "path_params": dict(request.path_params),
                "query_params": dict(request.query_params),
            },
        )

        # Process the request and get response
        try:
            response = await call_next(request)

            # Calculate request processing time
            process_time = time.time() - start_time

            # Log successful response
            logger.info(
                f"Completed {method} request to {url}",
                extra={
                    "status_code": response.status_code,
                    "process_time_ms": round(process_time * 1000, 2),
                    "headers": dict(response.headers),
                },
            )

            # Add processing time header
            response.headers["X-Process-Time"] = str(process_time)

            return response

        except Exception as e:
            # Log error response
            process_time = time.time() - start_time
            logger.error(
                f"Error processing {method} request to {url}: {str(e)}",
                extra={
                    "error": str(e),
                    "process_time_ms": round(process_time * 1000, 2),
                    "client_host": client_host,
                },
            )
            raise


def setup_logging_middleware(app: FastAPI) -> None:
    """Add logging middleware to FastAPI application."""
    app.add_middleware(BaseHTTPMiddleware, dispatch=APILoggingMiddleware(app).dispatch)
