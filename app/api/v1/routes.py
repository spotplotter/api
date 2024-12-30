from fastapi import APIRouter, File, UploadFile
from app.models.schemas import PredictionResponse
from app.services.predictions import predict

router = APIRouter()


@router.post("/predict", response_model=PredictionResponse)
async def predict_endpoint(file: UploadFile = File(...)):
    """Endpoint to handle predictions."""
    # Read the uploaded file
    contents = await file.read()

    # Pass the file contents to the prediction service
    prediction_result = predict(contents)

    return prediction_result
