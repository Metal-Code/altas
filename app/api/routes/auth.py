from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.auth_service import register_user, verify_otp, login_user, forgot_password, reset_password
from app.schemas.user import UserCreate, UserLogin, UserResponse, VerifyOTP, ForgotPassword, ResetPassword
from app.core.database import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
async def register_router(user_data : UserCreate,db : AsyncSession = Depends(get_db)):
     return await register_user(db, user_data)
    

@router.post("/verify-otp")
async def verify_router(data : VerifyOTP, db : AsyncSession = Depends(get_db)):
        return await verify_otp(db, data.email, data.otp)


@router.post("/login")
async def login_router(user_data : UserLogin, db : AsyncSession = Depends(get_db)):
        return await login_user(db, user_data.email, user_data.password)

@router.post("/forgot-password")
async def forgot_password_router(data : ForgotPassword, db : AsyncSession = Depends(get_db)):
       return await forgot_password(db, data.email)

@router.post("/reset-password")
async def reset_password_router(data : ResetPassword, db : AsyncSession = Depends(get_db)):
       return await reset_password(db, data.email, data.otp, data.new_password)