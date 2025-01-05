import os
from pydantic_settings import BaseSettings
from pydantic import SecretStr


class DatabaseSettings(BaseSettings):
    url: str = os.environ["DATABASE_URL"]


class EmailSettings(BaseSettings):
    username: str = os.environ["EMAIL_USERNAME"]
    password: SecretStr = SecretStr(os.environ["EMAIL_PASSWORD"])
    server: str = os.environ["EMAIL_SERVER"]
    port: int = int(os.environ["EMAIL_PORT"])
    from_address: str = os.environ["EMAIL_FROM"]
    start_tls: bool = True
    ssl_tls: bool = False
    use_credentials: bool = True


class Settings(BaseSettings):
    app_name: str = "SpotPlotter API"
    model_path: str = "resnet50.keras"
    base_url: str = os.environ["BASE_URL"]
    database_settings: DatabaseSettings = DatabaseSettings()
    email_settings: EmailSettings = EmailSettings()
    jwt_secret: str = os.environ["JWT_SECRET"]


settings = Settings()
