from fastapi import HTTPException
from app.models.pending_registration import PendingRegistration
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, date
 
async def create_pending_registration(db : AsyncSession, name : str, email : str, hashed_password : str, dob : date, location : str, gender : str, phone_number : str, otp : str, expires_at : datetime, avatar_url=None) -> PendingRegistration:
    pending_user = PendingRegistration(name=name, email=email, hashed_password=hashed_password, dob=dob, location=location, gender=gender, phone_number=phone_number, otp=otp, expires_at=expires_at, avatar_url=avatar_url)
    db.add(pending_user)
    await db.commit()
    await db.refresh(pending_user)
    return pending_user


async def get_pending_by_email(db : AsyncSession, email : str) -> PendingRegistration | None:
    result = await db.execute(select(PendingRegistration).where(PendingRegistration.email == email))
    return result.scalar_one_or_none()

async def update_otp(db : AsyncSession, pending : PendingRegistration, new_otp : str, new_expires_at : datetime) -> PendingRegistration:
    pending.otp = new_otp
    pending.expires_at = new_expires_at
    await db.commit()
    await db.refresh(pending)
    return pending

async def delete_pending(db : AsyncSession, pending : PendingRegistration):
    await db.delete(pending)
    await db.commit()
