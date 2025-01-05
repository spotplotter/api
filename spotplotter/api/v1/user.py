from fastapi import APIRouter, HTTPException, Depends
from spotplotter.models.user import UserRegisterSchema, UserResponseSchema
from spotplotter.services.user import create_user, get_user_by_email

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponseSchema)
async def register(user_data: UserRegisterSchema) -> UserResponseSchema:
    """Register a new user."""
    existing_user = await get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = await create_user(
        user_data.email, user_data.password, user_data.full_name
    )

    if not new_user:
        raise HTTPException(status_code=500, detail="User registration failed")

    return UserResponseSchema(
        id=new_user["id"],
        email=new_user["email"],
        full_name=new_user["full_name"],
    )
