from spotplotter.database import async_db
from spotplotter.core.jwt import create_verification_token, verify_token
from spotplotter.core.email import send_verification_email
import bcrypt


async def hash_password(password: str) -> str:
    """Hash the password using bcrypt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


async def create_user(email: str, password: str, full_name: str) -> dict:
    """Insert a new user into the database."""
    hashed_password = await hash_password(password)

    query = """
    INSERT INTO users (email, password_hash, full_name)
    VALUES ($1, $2, $3)
    RETURNING id, email, full_name, is_verified
    """
    new_user = await async_db.fetch_one(query, email, hashed_password, full_name)

    if new_user:
        token = create_verification_token(email)
        await send_verification_email(email, token)

    return new_user


async def get_user_by_email(email: str):
    """Fetch a user by email."""
    query = "SELECT id, email, full_name, password_hash FROM users WHERE email = $1"
    return await async_db.fetch_one(query, email)


async def verify_user_email(token: str):
    """Verify email and update the database."""
    email = verify_token(token)
    if not email:
        return None, "Invalid or expired token"

    query = "UPDATE users SET is_verified = TRUE WHERE email = $1 RETURNING email, is_verified"
    updated_user = await async_db.fetch_one(query, email)

    if not updated_user:
        return None, "User not found"

    return updated_user, None
