from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, EmailStr, model_validator, ConfigDict
from typing import Any


class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    is_admin: bool
    default_thread_id: int


class TokenData(BaseModel):
    email: Optional[EmailStr] = None


class UserLogin(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: EmailStr
    password: str


class UserBase(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: EmailStr


class UserCreate(UserBase):
    model_config = ConfigDict(extra="forbid")
    email: EmailStr
    full_name: str


class User(UserBase):
    id: int
    is_admin: bool

    class Config:
        from_attributes = True
