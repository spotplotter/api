import numpy as np

from app.core.config import settings
from dataclasses import dataclass
from tensorflow.keras.models import load_model
from app.models.cbam_layer import CBAM
from app.models.focal_loss import focal_loss


model = load_model(
    settings.model_path, custom_objects={"CBAM": CBAM, "focal_loss_fixed": focal_loss}
)


class_labels = {
    0: "melanoma",
    1: "nevus",
    2: "seborrheic keratosis",
    3: "basal cell carcinoma",
    4: "actinic keratosis",
    5: "vascular lesion",
    6: "dermatofibroma",
}


@dataclass
class Prediction:
    predicted_class: int
    predicted_class_name: str
    confidence: float


def predict_model(input_array) -> list[Prediction]:
    """
    Make predictions using the loaded model and return all classes with confidence scores.

    Args:
        input_array (np.ndarray): Preprocessed input data for the model.

    Returns:
        list[Prediction]: List of predictions with class indices and confidence scores.
    """
    # Get predictions from the model (softmax probabilities)
    predictions = model.predict(
        input_array, verbose=0
    )  # Shape: (batch_size, num_classes)

    # Extract probabilities for the first input in the batch
    probabilities = predictions[0]

    return [
        Prediction(
            predicted_class=i,
            predicted_class_name=class_labels[i],
            confidence=float(prob),
        )
        for i, prob in enumerate(probabilities)
    ]
