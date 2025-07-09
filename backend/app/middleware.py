from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse


class LimitUploadSizeMiddleware(BaseHTTPMiddleware):
    # This is a middleware to prevent big files uploaded
    def __init__(self, app, max_upload_size: int):
        super().__init__(app)
        self.max_upload_size = max_upload_size

    async def dispatch(self, request: Request, call_next):
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > self.max_upload_size:
            return JSONResponse(
                {
                    "detail": (
                        f"File size exceeds maximum allowed size of "
                        f"{self.max_upload_size} bytes."
                    )
                },
                status_code=413,
            )
        return await call_next(request)
