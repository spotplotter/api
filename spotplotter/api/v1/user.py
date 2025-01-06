from fastapi import APIRouter, HTTPException, Depends
from spotplotter.models.user import UserRegisterSchema, UserResponseSchema
from spotplotter.services.user import create_user, get_user_by_email, verify_user_email

router = APIRouter(prefix="/user", tags=["User"])


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
        is_verified=new_user["is_verified"],
    )


@router.get("/verify-email")
async def verify_email(token: str):
    """API route for email verification."""
    updated_user, error = await verify_user_email(token)

    if error:
        raise HTTPException(
            status_code=400 if "Invalid" in error else 404, detail=error
        )

    return {"message": "Email successfully verified!"}
