from sqlalchemy.ext.asyncio import AsyncSession
from app.models.refresh_token import RefreshToken
from sqlalchemy import select

async def get_refresh_token_repo(db : AsyncSession, token : str) -> RefreshToken | None:
    result = await db.execute(select(RefreshToken).where(RefreshToken.token == token))
    return result.scalar_one_or_none()
