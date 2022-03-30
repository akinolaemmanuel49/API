import datetime
from typing import List, Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    email: str
    password: str


class User(BaseModel):
    id: int
    username: str
    email: str
    active: bool
    is_admin: bool
    created: datetime.datetime
    last_modified: datetime.datetime

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    access_token: str
    refresh_token: str
    user_id: str


class Credentials(BaseModel):
    username: str
    password: str
