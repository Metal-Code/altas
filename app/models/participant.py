from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, func, ForeignKey, UniqueConstraint
from datetime import datetime, date
from app.core.database import Base

class Participant(Base):
    __tablename__ = 'participants'
    id : Mapped[int] = mapped_column(primary_key=True)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    activity_id : Mapped[int] = mapped_column(ForeignKey("activities.id"))
    joined_at : Mapped[datetime] = mapped_column(server_default=func.now())

    __table_args__ = (
        UniqueConstraint('user_id', 'activity_id', name='unique_user_activity'),
    )