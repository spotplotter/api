import numpy as np
from PIL import Image
from io import BytesIO
from app.models.tensorflow_model import predict_model, Prediction
from app.models.schemas import PredictionDetails, PredictionResponse


def predict(image_data: bytes):
    """Preprocess input image and make predictions."""
    # Load and preprocess the image
    image = Image.open(BytesIO(image_data)).convert("RGB")  # Ensure 3 channels (RGB)
    image = image.resize((224, 224))  # Resize to model input size
    input_array = np.expand_dims(
        np.array(image) / 255.0, axis=0
    )  # Normalize and add batch dimension

    # Get predictions from the model
    predictions = predict_model(input_array)

    # Create PredictionDetails objects for the response
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
