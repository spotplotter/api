from fastapi import FastAPI
from app.api.v1.routes import router as api_router

app = FastAPI(title="Inference API")

# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Inference API!"}
