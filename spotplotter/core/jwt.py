import jwt
import os
from datetime import datetime, timedelta, timezone

JWT_SECRET = os.environ["JWT_SECRET"]
JWT_ALGORITHM = "HS256"


def create_verification_token(email: str) -> str:
    """Generate a JWT token for email verification."""
    payload = {
        "sub": email,
        "exp": datetime.now(timezone.utc) + timedelta(hours=24),  # Token valid for 24h
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_token(token: str) -> str | None:
    """Decode JWT and return email."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
