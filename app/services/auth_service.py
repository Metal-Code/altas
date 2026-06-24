from fastapi import HTTPException
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserLogin
from app.repositories.user_repository import get_user_by_email, get_user_by_id
from app.models.user import User
from app.models.otp import EmailVerification
from sqlalchemy import select
from app.core.config import settings
from app.core.security import hash_password
from datetime import datetime, date, timedelta, timezone
import random

def generate_otp():
    return str(random.randint(100000, 999999))

async def register_user(db : AsyncSession, user_data : UserCreate):
    existing_user = await get_user_by_email(db, user_data.email)
    if existing_user:
        raise ValueError("Email already registered")
    
    otp = generate_otp()
    otp_expires_at = datetime.now(timezone.utc) + timedelta(seconds=settings.OTP_EXPIRY_SECONDS)
    hashed_password = hash_password(user_data.password)
    
    
    

    