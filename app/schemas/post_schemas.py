import datetime
from typing import List

from pydantic import BaseModel

from schemas.comment_schemas import Comment


class PostBase(BaseModel):
    post: str


class PostCreate(PostBase):
    owner_id: int


class PostUpdate(PostBase):
    pass


class Post(PostBase):
    id: int
    post: str
    owner_id: int

    comments: List[Comment] = []

    class Config:
        orm_mode = True
