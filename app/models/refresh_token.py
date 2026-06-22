from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Date, ForeignKey, Boolean, func
from datetime import datetime
from app.core.database import Base

class RefreshToken(Base):
    __tablename__ = "refresh_token"

    id : Mapped[int] = mapped_column(primary_key=True)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    token : Mapped[str] = mapped_column(String(500), unique=True)
    expires_at : Mapped[datetime] = mapped_column()
    revoked : Mapped[bool] = mapped_column(Boolean)
    created_at : Mapped[datetime] = mapped_column(server_default=func.now())