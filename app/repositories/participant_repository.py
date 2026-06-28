from app.core.database import get_db
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.activity import Activity
from app.models.user import User
from app.models.participant import Participant
from datetime import date, datetime
from fastapi import HTTPException

async def repo_join_activity(db : AsyncSession, user_id : int, activity_id : int) -> Participant:
    result = Participant(user_id=user_id, activity_id=activity_id)
    db.add(result)
    await db.commit()
    await db.refresh(result)
    return result  

async def repo_leave_activity(db : AsyncSession, participant : Participant):
    await db.delete(participant)    
    await db.commit()

async def repo_get_participants(db : AsyncSession, activity_id : int) -> list[Participant]:
    result = await db.execute(
        select(Participant).where(Participant.activity_id == activity_id)
    )
    return list(result.scalars().all())
    
async def repo_is_already_joined(db : AsyncSession, user_id : int, activity_id : int) -> Participant | None:
    result = await db.execute(
        select(Participant).where(
            Participant.user_id == user_id,
            Participant.activity_id == activity_id
            )
        )
    return result.scalar_one_or_none()

async def repo_is_activity_full(db : AsyncSession, activity_id : int) -> int:
    result = await db.execute(select(func.count()).select_from(Participant).where(Participant.activity_id == activity_id))
    return result.scalar()

