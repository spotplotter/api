from spotplotter.core.config import settings
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, SecretStr
import os


conf = ConnectionConfig(
    MAIL_USERNAME=settings.email_settings.username,
    MAIL_PASSWORD=settings.email_settings.password,
    MAIL_FROM=settings.email_settings.from_address,
    MAIL_PORT=settings.email_settings.port,
    MAIL_SERVER=settings.email_settings.server,
    MAIL_STARTTLS=settings.email_settings.start_tls,
    MAIL_SSL_TLS=settings.email_settings.ssl_tls,
    USE_CREDENTIALS=settings.email_settings.use_credentials,
)


async def send_verification_email(email: EmailStr, token: str):
    """Send verification email with JWT token link."""
    verify_url = f"{settings.base_url}/api/v1/verify-email?token={token}"

    message = MessageSchema(
        subject="Verify Your Email",
        recipients=[email],
        body=f"Click the link to verify your email: {verify_url}",
        subtype=MessageType.html,
    )

    fm = FastMail(conf)
    await fm.send_message(message)
