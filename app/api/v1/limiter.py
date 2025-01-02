from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address

# Create a global Limiter instance
limiter = Limiter(
    key_func=get_remote_address,
    headers_enabled=True,
    default_limits=["10/minute"],
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
