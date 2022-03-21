from typing import List

from fastapi import APIRouter, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

import dependencies

from db.dals import reply_dal
from db.dals.user_dal import auth_handler
from schemas import comment_schemas

security = HTTPBearer()

router = APIRouter(prefix="/replies")


@router.post("/", response_model=comment_schemas.Comment)
def create_reply(post_id: int, parent_id: int, reply: comment_schemas.ReplyCreate, db: Session = Depends(dependencies.get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
    access_token = credentials.credentials
    user_id = auth_handler.decode_token(access_token)
    db_reply = reply_dal.create_reply(
        owner_id=user_id, post_id=post_id, parent_id=parent_id, db=db, reply=reply)
    return db_reply


@router.get("/{comment_id}", response_model=List[comment_schemas.Comment])
def get_replies_by_comment(comment_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)):
    db_replies = reply_dal.get_replies_by_comment(
        db=db, comment_id=comment_id, skip=skip, limit=limit)
    return db_replies
