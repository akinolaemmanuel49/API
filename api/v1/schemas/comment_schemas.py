import datetime
from typing import List

from pydantic import BaseModel

# from schemas.reply_schemas import Reply


class CommentBase(BaseModel):
    comment: str


class CommentCreate(CommentBase):
    pass


class CommentUpdate(CommentBase):
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


class ReplyUpdate(ReplyBase):
    pass
