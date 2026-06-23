from app.core.database import get_db
from sqlalchemy import select
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from datetime import date, datetime

async def get_user_by_email(db : AsyncSession, email : str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def get_user_by_id(db : AsyncSession, id : int) -> User | None:
    result = await db.execute(select(User).where(User.id == id))
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, name: str, email: str, hashed_password: str, dob: date, location: str, gender: str, phone_number: str | None = None, avatar_url: str | None = None) -> User:
    user = User(name=name, email=email, hashed_password=hashed_password, dob=dob, location=location, gender=gender, phone_number=phone_number, avatar_url=avatar_url)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user