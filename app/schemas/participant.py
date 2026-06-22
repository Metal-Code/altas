from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional

class ParticipantCreate(BaseModel):
    activity_id : int

class ParticipantResponse(BaseModel):
    id : int
    user_id : int
    activity_id : int
    joined_at : datetime
    model_config = ConfigDict(from_attributes=True)