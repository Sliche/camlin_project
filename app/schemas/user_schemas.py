import re
from datetime import datetime
from pydantic import EmailStr, Field, field_validator
from typing import Optional

from app.schemas.base_schema import BaseSchema


class UserCreate(BaseSchema):
    username: str = Field(
        ...,
        min_length=3,
        max_length=20,
        description="Username must be 3–20 characters long, only lowercase letters"
    )
    password: str = Field(
        ...,
        min_length=8,
        description="Password must be at least 8 characters long"
    )
    email: EmailStr = Field(
        ...,
        description="Valid email address"
    )
    first_name: Optional[str] = Field(
        None,
        max_length=30,
        description="Optional first name (max 30 characters)"
    )
    last_name: Optional[str] = Field(
        None,
        max_length=30,
        description="Optional last name (max 30 characters)"
    )

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        if not re.fullmatch(r"[a-zA-Z0-9]+", value):
            raise ValueError("Username must contain only letters and numbers (no symbols or spaces).")
        return value


class UpdateUserSchema(UserCreate):
    pass


class UserResponse(BaseSchema):
    id: int
    username: str
    email: EmailStr

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class UserSchema(BaseSchema):
    id: int

    username: str
    password: str
    email: EmailStr

    first_name: Optional[str] = None
    last_name: Optional[str] = None