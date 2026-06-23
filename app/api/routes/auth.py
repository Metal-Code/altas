from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.core.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse

