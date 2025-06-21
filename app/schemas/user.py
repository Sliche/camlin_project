from pydantic import BaseModel, EmailStr
from typing import Optional


class UserSchema(BaseModel):
    id: int

    username: str
    password: str
    email: EmailStr

    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr

    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    first_name: Optional[str] = None
    last_name: Optional[str] = None

    # class Config:
    #     orm_mode = True
