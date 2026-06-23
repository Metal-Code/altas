from fastapi import HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_token
from app.core.database import get_db
from app.models.user import User
from sqlalchemy import select

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(db : AsyncSession = Depends(get_db), token : str = Depends(oauth2_scheme)):
    try:
        temp_token = decode_token(token)
    except:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user_id = temp_token.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401)

    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=401)

    return user


