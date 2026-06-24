from fastapi import HTTPException
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserLogin
from app.repositories.user_repository import get_user_by_email, get_user_by_id, create_user
from app.repositories.pending_registration_repository import create_pending_registration, delete_pending, update_otp, get_pending_by_email
from app.models.user import User
from app.models.refresh_token import RefreshToken
from sqlalchemy import select
from app.core.config import settings
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from datetime import datetime, date, timedelta, timezone
from app.models.pending_registration import PendingRegistration
from datetime import date, datetime, timezone
import random

def generate_otp():
    return str(random.randint(100000, 999999))

async def register_user(db : AsyncSession, user_data : UserCreate):
    existing_user = await get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    otp = generate_otp()
    otp_expires_at = datetime.now(timezone.utc) + timedelta(seconds=settings.OTP_EXPIRY_SECONDS)
    hashed_pwd = hash_password(user_data.password)

    existing_pending_user = await get_pending_by_email(db, user_data.email)
    if existing_pending_user:
        await update_otp(db, existing_pending_user, new_otp=otp, new_expires_at=otp_expires_at)
        print(otp)
        return {
            "message" : "OTP sent to your email"
        }
    await create_pending_registration(
        db,
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_pwd,
        dob=user_data.dob,
        location=user_data.location,
        gender=user_data.gender,
        phone_number=user_data.phone_number,
        otp=otp,
        expires_at=otp_expires_at,
        avatar_url=user_data.avatar
    )

    print(otp)
    return {"message": "OTP sent to your email"}


async def verify_otp(db : AsyncSession, email : str, otp_code : str):
    pending = await get_pending_by_email(db, email)
    if not pending:
        raise HTTPException(status_code=400, detail="User not registered yet")
    
    if datetime.now(timezone.utc) > pending.expires_at:
        raise HTTPException(status_code=400, detail="OTP has expired")
    
    if otp_code != pending.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    user = await create_user(
        db,
        name=pending.name,
        email=pending.email,
        hashed_password=pending.hashed_password,
        dob=pending.dob,
        location=pending.location,
        gender=pending.gender,
        phone_number=pending.phone_number,
        avatar_url=pending.avatar_url
    )
    await delete_pending(db, pending)
    return user


async def login_user(db : AsyncSession, email : str, password : str):
    existing_user = await get_user_by_email(db, email)
    if not existing_user:
        raise HTTPException(status_code=401, detail= "Invalid credentials")
    if not verify_password(password, existing_user.hashed_password):
        raise HTTPException(status_code=401, detail= "Invalid credentials")
    
    access_token = create_access_token(data={
        "sub" : str(existing_user.id)
    })
    
    refresh_token = create_refresh_token(data={
        "sub" : str(existing_user.id)
    })

    db_refresh_token = RefreshToken(
        user_id = existing_user.id,
        token = refresh_token,
        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    db.add(db_refresh_token)
    await db.commit()
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

async def forgot_password(db : AsyncSession, email : str):
    user = await get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    otp = generate_otp()
    otp_expires_at = datetime.now(timezone.utc) + timedelta(seconds=settings.OTP_EXPIRY_SECONDS)

    pending_user = await get_pending_by_email(db, email)
    if pending_user:
        await update_otp(db, pending_user, otp, otp_expires_at)
    else:
        await create_pending_registration(
            db,
            name=user.name,
            email=user.email,
            hashed_password=user.hashed_password,
            dob=user.dob,
            location=user.location,
            gender=user.gender,
            phone_number=user.phone_number,
            otp=otp,
            expires_at=otp_expires_at,
            avatar_url=user.avatar_url
        )
    print(otp)
    return {
        "message" : "OTP sent to verify and change password"
    }

async def reset_password(db : AsyncSession, email : str, otp_code : str, new_password : str):
    pending = await get_pending_by_email(db, email)
    if not pending:
        raise HTTPException(status_code=400, detail="something went wrong")
    
    if datetime.now(timezone.utc) > pending.expires_at:
        raise HTTPException(status_code=400, detail="OTP has expired")

    if otp_code != pending.otp:
        raise HTTPException(status_code=401, detail="OTP is invalid")
    

    real_user = await get_user_by_email(db, email)
    real_user.hashed_password = hash_password(new_password)
    await db.commit()
    await delete_pending(db, pending)
    return {
        "message" : "Password reset successfully"
    }