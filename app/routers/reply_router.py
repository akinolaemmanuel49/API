from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import dependencies
from db.dals import reply_dal
from schemas import comment_schemas

router = APIRouter(prefix="/replies")


@router.post("/", response_model=comment_schemas.Comment)
def create_reply(reply: comment_schemas.ReplyCreate, db: Session = Depends(dependencies.get_db)):
    db_reply = reply_dal.create_reply(db=db, reply=reply)
    print(reply)
    return db_reply


@router.get("/{comment_id}", response_model=List[comment_schemas.Comment])
def get_replies_by_comment(comment_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)):
    db_replies = reply_dal.get_replies_by_comment(
        db=db, comment_id=comment_id, skip=skip, limit=limit)
    return db_replies
