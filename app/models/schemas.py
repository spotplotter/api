from pydantic import BaseModel
from typing import List


class PredictionRequest(BaseModel):
    input_data: List[float]


class PredictionDetails(BaseModel):
    predicted_class: str
    confidence: float


class PredictionResponse(BaseModel):
    predictions: list[PredictionDetails]
    best_prediction: PredictionDetails
