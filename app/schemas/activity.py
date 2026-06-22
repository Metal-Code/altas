from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional


class ActivityCreate(BaseModel):
    title : str
    description : str
    location : str
    max_participants : int
    date_time : datetime
    category : str

class ActivityResponse(BaseModel):
    id : int
    creator_id : int
    created_at : datetime
    title : str
    description : str
    location : str
    max_participants : int
    date_time : datetime
    category : str
    model_config = ConfigDict(from_attributes=True)

class ActivityUpdate(BaseModel):
    title : Optional[str] = None
    description : Optional[str] = None
    location : Optional[str] = None
    max_participants : Optional[int] = None
    date_time : Optional[datetime] = None
    category : Optional[str] = None