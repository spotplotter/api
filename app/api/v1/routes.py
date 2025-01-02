from fastapi import APIRouter, File, UploadFile, HTTPException
from app.models.schemas import PredictionResponse
from app.services.predictions import predict

router = APIRouter()


@router.post("/predict", response_model=PredictionResponse)
async def predict_endpoint(file: UploadFile = File()):
    """Endpoint to handle predictions using streaming."""
    try:
        file_bytes = file.file

        prediction_result = predict(file_bytes)

        return prediction_result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
