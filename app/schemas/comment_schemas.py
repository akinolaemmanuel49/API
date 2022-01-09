from typing import List

from pydantic import BaseModel

# from schemas.reply_schemas import Reply


class CommentBase(BaseModel):
    comment: str


class CommentCreate(CommentBase):
    owner_id: int
    post_id: int


class CommentUpdate(CommentBase):
    pass


class Comment(BaseModel):
    id: int
    comment: str
    owner_id: int
    post_id: int

    replies: List = []

    class Config:
        orm_mode = True


class ReplyBase(BaseModel):
    reply: str


class ReplyCreate(ReplyBase):
    owner_id: int
    post_id: int
    parent_id: int
