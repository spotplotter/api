import os
from pydantic_settings import BaseSettings
from pydantic import SecretStr


class DatabaseSettings(BaseSettings):
    url: str = os.environ["DATABASE_URL"]


class EmailSettings(BaseSettings):
    sendgrid_api_key: SecretStr = SecretStr(os.environ["SENDGRID_API_KEY"])
    from_address: str = os.environ["EMAIL_FROM_ADDRESS"]


class Settings(BaseSettings):
    app_name: str = "SpotPlotter API"
    model_path: str = "resnet50.keras"
    base_url: str = os.environ["BASE_URL"]
    database_settings: DatabaseSettings = DatabaseSettings()
    email_settings: EmailSettings = EmailSettings()
    jwt_secret: str = os.environ["JWT_SECRET"]


settings = Settings()
