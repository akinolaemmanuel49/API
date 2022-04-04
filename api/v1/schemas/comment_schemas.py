import datetime
from typing import List

from pydantic import BaseModel


class CommentBase(BaseModel):
    comment: str


class CommentCreate(CommentBase):
    pass

    class Config:
        schema_extra = {
            "example": {
                "comment": "This is my first comment",
            }
        }


class CommentUpdate(CommentCreate):
    pass


class Comment(BaseModel):
    id: int
    comment: str
    owner_id: int
    post_id: int
    created: datetime.datetime
    last_modified: datetime.datetime

    replies: List = None

    class Config:
        orm_mode = True


class ReplyBase(BaseModel):
    reply: str


class ReplyCreate(ReplyBase):
    pass

    class Config:
        schema_extra = {
            "example": {
                "reply": "This is my first reply",
            }
        }


class ReplyUpdate(ReplyCreate):
    pass
