from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime, date
from typing import Optional

class UserCreate(BaseModel):
    name : str
    email : EmailStr
    password : str
    avatar : Optional[str] = None
    dob : date
    location : str
    gender : str

class UserLogin(BaseModel):
    email : EmailStr
    password : str

class UserResponse(BaseModel):
    id : int
    name : str
    email : EmailStr
    dob : date
    phone_number : str
    avatar_url : Optional[str] = None
    location : str
    gender : str
    model_config = ConfigDict(from_attributes=True)

