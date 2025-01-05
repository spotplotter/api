from fastapi import Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address


def xff_key_func(request: Request):
    xff = request.headers.get("X-Forwarded-For")

    if xff:
        return xff.split(",")[0].strip()

    return get_remote_address(request)


# Create a global Limiter instance
limiter = Limiter(
    key_func=xff_key_func,
    headers_enabled=True,
    default_limits=["20/minute"],
    strategy="moving-window",
    # TODO: Redis
    storage_uri="memory://",
)


# Define the rate limit exceeded handler
def rate_limit_exceeded_handler(request, exc) -> JSONResponse:
    return JSONResponse(
        content={"detail": "Rate limit exceeded. Too many requests."},
        status_code=429,
    )
