from spotplotter.database import async_db
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
    RETURNING id, email, full_name
    """
    return await async_db.fetch_one(query, email, hashed_password, full_name)


async def get_user_by_email(email: str):
    """Fetch a user by email."""
    query = "SELECT id, email, full_name, password_hash FROM users WHERE email = $1"
    return await async_db.fetch_one(query, email)
