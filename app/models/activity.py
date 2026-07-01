from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, func, ForeignKey
from datetime import datetime, date
from app.core.database import Base
import uuid as uuid_module
from sqlalchemy import UUID

class Activity(Base):
    __tablename__ = "activities"
    
    id : Mapped[int] = mapped_column(primary_key=True)
    public_id: Mapped[uuid_module.UUID] = mapped_column(UUID(as_uuid=True), default=uuid_module.uuid4, unique=True, index=True)
    creator_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    title : Mapped[str] = mapped_column(String(100), nullable=False)
    description : Mapped[str | None] = mapped_column(String(800), nullable=True)
    location : Mapped[str] = mapped_column(String(100), nullable=False)
    date_time : Mapped[datetime] = mapped_column()
    max_participants : Mapped[int | None] = mapped_column()
    category : Mapped[str | None] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())