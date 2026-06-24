from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Date, func
from datetime import date, datetime
from app.core.database import Base

class PendingRegistration(Base):
    __tablename__ = "pending_registration"

    id : Mapped[int] = mapped_column(primary_key=True)
    email : Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    phone_number: Mapped[str] = mapped_column(String(20))
    hashed_password: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    dob: Mapped[date] = mapped_column(Date)
    avatar_url: Mapped[str | None] = mapped_column(String(1000), default=None)
    gender : Mapped[str] = mapped_column(String(15))
    location : Mapped[str] = mapped_column(String(50))
    otp : Mapped[str] = mapped_column(String(10))
    expires_at : Mapped[datetime] = mapped_column()
    created_at : Mapped[datetime] = mapped_column(server_default=func.now())