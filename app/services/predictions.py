import numpy as np
from PIL import Image
from typing import BinaryIO
from app.models.tensorflow_model import predict_model, Prediction
from app.models.schemas import PredictionDetails, PredictionResponse


def predict(image_stream: BinaryIO):
    """Preprocess input image from a stream and make predictions."""
    try:
        image = Image.open(image_stream).convert("RGB")
        image = image.resize((224, 224))
        input_array = np.expand_dims(np.array(image) / 255.0, axis=0)

        predictions = predict_model(input_array)

        prediction_details = [
            PredictionDetails(
                predicted_class=pred.predicted_class_name,
                confidence=pred.confidence,
            )
            for pred in predictions
        ]

        best_prediction = max(prediction_details, key=lambda pred: pred.confidence)

        return PredictionResponse(
            predictions=prediction_details, best_prediction=best_prediction
        )
    except Exception as e:
        raise ValueError(f"Error processing the image: {e}")
