from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from spotplotter.api.v1.predict import router as predict_router
from spotplotter.api.v1.user import router as user_router
from spotplotter.api.v1.limiter import limiter, rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager
from spotplotter.database import async_db
from spotplotter.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown with asyncpg"""
    await async_db.connect()
    yield  # This keeps the app running
    await async_db.disconnect()


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://spotplotter.com",
    ],
    allow_credentials=True,
    allow_methods=["POST", "GET", "PATCH", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

# Include API routes
app.include_router(user_router, prefix="/api/v1")
app.include_router(predict_router, prefix="/api/v1")


@app.get("/")
def read_root(request: Request) -> JSONResponse:
    return JSONResponse(content={"message": "Inference API"})
