from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Inference API!"}


def test_prediction():
    response = client.post("/api/v1/predict", json={"input_data": [0.1, 0.2, 0.3, 0.4]})
    assert response.status_code == 200
    assert "predictions" in response.json()
