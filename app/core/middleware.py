import time
from typing import Callable

from fastapi import FastAPI, Request, Response
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging request information"""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        # Process the request
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            
            # Log request details
            logger.info(
                f"{request.method} {request.url.path} "
                f"[{response.status_code}] "
                f"{process_time:.4f}s"
            )
            
            # Add custom header with processing time
            response.headers["X-Process-Time"] = str(process_time)
            return response
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(
                f"{request.method} {request.url.path} "
                f"[500] "
                f"{process_time:.4f}s "
                f"Error: {str(e)}"
            )
            raise


def setup_middleware(app: FastAPI) -> None:
    """Configure middleware for the application"""
    app.add_middleware(RequestLoggingMiddleware)
