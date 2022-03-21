import datetime
from typing import List

from pydantic import BaseModel

from app.schemas.comment_schemas import Comment


class PostBase(BaseModel):
    post: str


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class Post(PostBase):
    id: int
    post: str
    owner_id: int
    created: datetime.datetime
    last_modified: datetime.datetime

    comments: List[Comment] = None

    class Config:
        orm_mode = True
