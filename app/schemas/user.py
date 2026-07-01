from pydantic import BaseModel, EmailStr, ConfigDict, field_validator
from datetime import datetime, date
from typing import Optional
import uuid as uuid_module
from sqlalchemy import UUID
import uuid

class UserCreate(BaseModel):
    name : str
    email : EmailStr
    password : str
    avatar : Optional[str] = None
    dob : date
    location : str
    gender : str
    phone_number : str

class UserLogin(BaseModel):
    email : EmailStr
    password : str

class UserResponse(BaseModel):
    public_id: uuid_module.UUID
    name : str
    email : EmailStr
    dob : date
    phone_number : str
    avatar_url : Optional[str] = None
    location : str
    gender : str
    model_config = ConfigDict(from_attributes=True)

class VerifyOTP(BaseModel):
    email : EmailStr
    otp : str

class ForgotPassword(BaseModel):
    email : EmailStr

class ResetPassword(BaseModel):
    email : EmailStr
    otp : str
    new_password : str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshToken(BaseModel):
    refresh_token : str

class RefreshTokenRequest(BaseModel):
    refresh_token: str


@field_validator("password")
@classmethod
def validate_password(cls, value: str) -> str:
    if len(value) < 6:
        raise ValueError("Password must be at least 6 characters")
    
    if not any(char.isupper() for char in value):
        raise ValueError("Password must contain at least one uppercase letter")
        
    if not any(char.islower() for char in value):
        raise ValueError("Password must contain at least one lowercase letter")
        
    if not any(char.isdigit() for char in value):
        raise ValueError("Password must contain at least one digit")
        
    return value