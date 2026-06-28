from fastapi import HTTPException
from app.schemas.participant import ParticipantCreate, ParticipantResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.participant_repository import repo_get_participants, repo_is_activity_full, repo_is_already_joined, repo_join_activity, repo_leave_activity
from app.models.activity import Activity
from app.models.participant import Participant
from app.models.user import User
from app.repositories.activity_repository import get_activity_by_id
from datetime import datetime, date

async def join_activity_service(db : AsyncSession, activity_id : int, current_user : User):
    activity = await get_activity_by_id(db, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity does not exist")
    
    is_joined = await repo_is_already_joined(db, current_user.id, activity_id)
    if is_joined:
        raise HTTPException(status_code=400, detail="Activity already joined")
    
    if datetime.utcnow() > activity.date_time:
        raise HTTPException(status_code=400, detail="Activity already expired")
    
    if activity.max_participants is not None:
        count = await repo_is_activity_full(db, activity.id)
        if count >= activity.max_participants:
            raise HTTPException(status_code=400, detail="Activity is full")
        
    joined_participant = await repo_join_activity(db, current_user.id, activity_id)
    return joined_participant
    

async def leave_activity_service(db : AsyncSession, activity_id : int, current_user : User):
    activity = await get_activity_by_id(db, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity does not exist")
    
    participant = await repo_is_already_joined(db, current_user.id, activity_id)
    if not participant:
        raise HTTPException(status_code=400, detail="Activity not joined")
    await repo_leave_activity(db, participant)
    return {
        "message" : "Activity left successfully"
    }

async def get_participants_service(db : AsyncSession, activity_id : int):
    activity = await get_activity_by_id(db, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity does not exist")
    result = await repo_get_participants(db, activity_id)
    return result

async def remove_participant_service(db : AsyncSession, activity_id : int, target_user_id : int, current_user : User):
    activity = await get_activity_by_id(db, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity does not exist")
    
    if activity.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not Authorized")
    
    existing_user = await repo_is_already_joined(db, target_user_id, activity_id)
    if not existing_user:
        raise HTTPException(status_code=400, detail="The user is not a participant")
    
    await repo_leave_activity(db, existing_user)
    return {
        "message" : "Participant removed successfully"
    }

