import re
import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, validator


class ProfileBase(BaseModel):
    pass


class ProfileCreate(ProfileBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[datetime.date] = None
    profile_type: str

    class Config:
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "date_of_birth": datetime.date(year=1990, month=1, day=1),
                "profile_type": "personal"
            }
        }


class ProfileUpdate(ProfileCreate):
    pass


class Profile(BaseModel):
    id: int
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[datetime.date] = None
    profile_image: Optional[str] = None
    profile_type: str
    owner_id: int
    created: datetime.datetime
    last_modified: datetime.datetime

    class Config:
        orm_mode: True
