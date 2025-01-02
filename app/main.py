from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.v1.routes import router as api_router
from app.api.v1.limiter import limiter, rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

app = FastAPI(title="Inference API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def read_root(request: Request) -> JSONResponse:
    return JSONResponse(content={"message": "Inference API"})
