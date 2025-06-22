from app.schemas.base_schema import BaseSchema
from pydantic import BaseModel, EmailStr
from typing import Optional


class UserSchema(BaseSchema):
    id: int

    username: str
    password: str
    email: EmailStr

    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserCreate(BaseSchema):
    username: str
    password: str
    email: EmailStr

    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UpdateUserSchema(BaseSchema):
    username: Optional[str] = None
    email: Optional[EmailStr] = None

    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserResponse(BaseSchema):
    id: int
    username: str
    email: EmailStr

    first_name: Optional[str] = None
    last_name: Optional[str] = None
