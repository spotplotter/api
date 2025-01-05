from fastapi import APIRouter, File, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse
from spotplotter.models.predict import PredictionResponse
from spotplotter.services.predict import predict
from spotplotter.api.v1.limiter import limiter

router = APIRouter()


@router.post("/predict", response_model=PredictionResponse)
@limiter.limit("5/minute")
async def predict_endpoint(request: Request, file: UploadFile = File()) -> JSONResponse:
    """Endpoint to handle predictions using streaming."""
    try:
        # Access file bytes directly from the stream
        file_bytes = file.file

        # Make a prediction using the uploaded file
        prediction_result = predict(file_bytes)

        return JSONResponse(prediction_result.model_dump())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
