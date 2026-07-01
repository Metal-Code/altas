from fastapi import HTTPException, Depends, APIRouter, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.auth_service import register_user, verify_otp, login_user, forgot_password, reset_password
from app.schemas.user import UserCreate, UserLogin, UserResponse, VerifyOTP, ForgotPassword, ResetPassword, TokenResponse
from app.core.database import get_db
from app.core.limiter import limiter
import uuid

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
@limiter.limit("2/minute")
async def register_router(request : Request, user_data : UserCreate,db : AsyncSession = Depends(get_db)):
     return await register_user(db, user_data)
    

@router.post("/verify-otp", response_model=UserResponse)
@limiter.limit("5/minute")
async def verify_router(request : Request, data : VerifyOTP, db : AsyncSession = Depends(get_db)):
        return await verify_otp(db, data.email, data.otp)


@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")
async def login_router(request : Request, user_data : UserLogin, db : AsyncSession = Depends(get_db)):
        return await login_user(db, user_data.email, user_data.password)


@router.post("/forgot-password")
@limiter.limit("3/hour")
async def forgot_password_router(request : Request, data : ForgotPassword, db : AsyncSession = Depends(get_db)):
       return await forgot_password(db, data.email)


@router.post("/reset-password")
@limiter.limit("2/hour")
async def reset_password_router(request : Request, data : ResetPassword, db : AsyncSession = Depends(get_db)):
       return await reset_password(db, data.email, data.otp, data.new_password)