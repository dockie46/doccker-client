# middleware/logging.py
import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# Configure logging
logging.basicConfig(
    filename="app.log",  # Log file path
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000

        log_data = {
            "method": request.method,
            "url": str(request.url),
            "status_code": response.status_code,
            "duration_ms": round(process_time, 2),
            "client_ip": request.client.host if request.client else "unknown",
        }

        logging.info(log_data)
        return response
