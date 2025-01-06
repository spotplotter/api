import os
import sendgrid
from sendgrid.helpers.mail import Mail
from spotplotter.core.config import settings
from pydantic import EmailStr


sg = sendgrid.SendGridAPIClient(
    api_key=settings.email_settings.sendgrid_api_key.get_secret_value()
)


async def send_verification_email(email: EmailStr, token: str):
    """Send verification email using SendGrid API."""
    verify_url = f"{settings.base_url}/verify-email?token={token}"

    message = Mail(
        from_email=settings.email_settings.from_address,
        to_emails=email,
        subject="PlotSpotter: Verify Your Email",
        html_content=f"""
            <p>Click the link below to verify your email:</p>
            <p><a href="{verify_url}">{verify_url}</a></p>
            <p>If you didn't request this, please ignore this email.</p>
        """,
    )

    try:
        response = sg.send(message)
    except Exception as e:
        print(f"Failed to send email: {e}")
