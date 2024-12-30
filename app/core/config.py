from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Inference API"
    model_path: str = "resnet50.keras"


settings = Settings()
