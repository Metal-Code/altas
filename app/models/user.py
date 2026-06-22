from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Date
from datetime import date
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email : Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    phone_number: Mapped[str | None] = mapped_column(String(20))
    hashed_password: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    dob: Mapped[date] = mapped_column(Date)
    avatar_url: Mapped[str | None] = mapped_column(String(1000), default=None)