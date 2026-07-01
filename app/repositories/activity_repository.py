from sqlalchemy import select
from fastapi import HTTPException
from datetime import datetime, date
from app.models.activity import Activity
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.activity import ActivityUpdate
import uuid

async def get_activity_by_id(db : AsyncSession, id : int) -> Activity | None:
    result = await db.execute(select(Activity).where(Activity.id == id))
    return result.scalar_one_or_none()

async def create_activity(db: AsyncSession, creator_id: int, title: str, location: str, date_time: datetime, description: str | None = None, max_participants: int | None = None, category: str | None = None) -> Activity:
    activity = Activity(
        creator_id = creator_id,
        title = title,
        location = location,
        date_time = date_time,
        description = description,
        max_participants = max_participants,
        category=category
    )   
    db.add(activity)
    await db.commit()
    await db.refresh(activity)
    return activity

async def get_all_activities(db : AsyncSession, location : str | None = None):
    query = select(Activity)
    if location:
        query = query.where(Activity.location == location)
    result = await db.execute(query)
    return list(result.scalars().all())

async def update_activity(db : AsyncSession, activity, data : ActivityUpdate):
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(activity, field, value)
    await db.commit()
    await db.refresh(activity)
    return activity

async def delete_activity(db : AsyncSession, activity):
    await db.delete(activity)
    await db.commit()

async def get_activity_by_public_id(db: AsyncSession, public_id: uuid.UUID) -> Activity | None:
    result = await db.execute(select(Activity).where(Activity.public_id == public_id))
    return result.scalar_one_or_none()