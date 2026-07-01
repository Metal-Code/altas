from pydantic import BaseModel, EmailStr, ConfigDict
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