from pydantic import BaseModel, EmailStr, Field
from uuid import UUID


class UserRegisterSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., min_length=3, max_length=100)


class UserResponseSchema(BaseModel):
    id: UUID
    email: EmailStr
    full_name: str

    class Config:
        from_attributes = True
