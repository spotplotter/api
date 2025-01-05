import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "SpotPlotter API"
    model_path: str = "resnet50.keras"
    database_url: str = os.environ["DATABASE_URL"]
    jwt_secret: str = os.environ["JWT_SECRET"]


settings = Settings()
