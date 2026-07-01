from fastapi import Depends, APIRouter, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.activity_service import create_activity_service, update_activity_service, delete_activity_service, get_activities_service, get_activity_service
from app.schemas.activity import ActivityCreate, ActivityResponse, ActivityUpdate
from app.services.participant_service import join_activity_service, leave_activity_service, get_participants_service, remove_participant_service
from app.models.user import User
from app.schemas.participant import ParticipantCreate, ParticipantResponse
from app.models.participant import Participant
from app.core.database import get_db
from app.api.deps import get_current_user
from app.core.limiter import limiter
import uuid

router = APIRouter(prefix="/activity", tags=["Activity"])

@router.post("/", response_model=ActivityResponse)
@limiter.limit("10/minute")
async def create_activity(request: Request, activity_data: ActivityCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await create_activity_service(db, activity_data, current_user)


@router.get("/", response_model=list[ActivityResponse])
async def get_activities(location: str | None = None, db: AsyncSession = Depends(get_db)):
    return await get_activities_service(db, location)


@router.post("/{activity_id}/join", response_model=ParticipantResponse)
@limiter.limit("10/minute")
async def join_activity(request: Request, activity_id: uuid.UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> Participant:
    return await join_activity_service(db, activity_id, current_user)


@router.delete("/{activity_id}/leave")
async def leave_participants(activity_id: uuid.UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await leave_activity_service(db, activity_id, current_user)


@router.get("/{activity_id}/get-participants", response_model=list[ParticipantResponse])
async def show_participants(activity_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await get_participants_service(db, activity_id)


@router.delete("/{activity_id}/participants/{user_id}")
async def remove_participant(activity_id: uuid.UUID, user_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await remove_participant_service(db, activity_id, user_id, current_user)


@router.get("/{activity_id}", response_model=ActivityResponse)
async def get_activity(activity_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await get_activity_service(db, activity_id)


@router.patch("/{activity_id}", response_model=ActivityResponse)
async def update_activity(activity_id: uuid.UUID, activity_data: ActivityUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await update_activity_service(db, activity_id, activity_data, current_user)


@router.delete("/{activity_id}")
async def delete_activity(activity_id: uuid.UUID, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await delete_activity_service(db, activity_id, current_user)