from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.activity_repository import ( 
    get_all_activities as repo_get_all_activities, 
    update_activity as repo_update_activity, 
    delete_activity as repo_delete_activity, 
    create_activity as repo_create_activity,
    get_activity_by_public_id as repo_get_activity_by_public_id
    )
from app.schemas.user import UserCreate
from app.models.user import User
from datetime import datetime, date
from app.core.config import settings
from app.schemas.activity import ActivityCreate, ActivityUpdate, ActivityResponse
import uuid

async def create_activity_service(db : AsyncSession, activity_data : ActivityCreate, current_user : User):
    created_activity = await repo_create_activity(
        db,
        creator_id=current_user.id,
        title = activity_data.title,
        location=activity_data.location,
        date_time=activity_data.date_time.replace(tzinfo=None),
        description=activity_data.description,
        max_participants=activity_data.max_participants,
        category=activity_data.category
    )
    return created_activity

async def update_activity_service(db : AsyncSession, activity_id : uuid.UUID, activity_data : ActivityUpdate, current_user : User):
    activity = await repo_get_activity_by_public_id(db, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found!!!")
    if activity.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not Authorized")
    
    return await repo_update_activity(db, activity, activity_data)


async def delete_activity_service(db : AsyncSession, activity_id : uuid.UUID, current_user : User):
    activity = await repo_get_activity_by_public_id(db, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    if activity.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not Authorized")
    
    await repo_delete_activity(db, activity)
    return {
        "message" : "Activity deleted"
    }


async def get_activity_service(db : AsyncSession, activity_id : uuid.UUID):
    activity = await repo_get_activity_by_public_id(db, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity

async def get_activities_service(db : AsyncSession, location=None):
    return await repo_get_all_activities(db, location)