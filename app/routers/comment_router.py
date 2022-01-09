from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import dependencies
from db.dals import comment_dal
from schemas import comment_schemas

router = APIRouter(prefix="/comments")


@router.post("/", response_model=comment_schemas.Comment)
def create_comment(comment: comment_schemas.CommentCreate, db: Session = Depends(dependencies.get_db)):
    db_comment = comment_dal.create_comment(db=db, comment=comment)
    return db_comment


@router.get("/post/{post_id}", response_model=List[comment_schemas.Comment])
def get_comments_by_post(post_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)):
    db_comments = comment_dal.get_comments_by_post(
        db=db, post_id=post_id, skip=skip, limit=limit)
    return db_comments


@router.get("/user/{owner_id}", response_model=List[comment_schemas.Comment])
def get_all_user_comments(owner_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)):
    db_user_comments = comment_dal.get_all_user_comments(
        db=db, user_id=owner_id, skip=skip, limit=limit)
    return db_user_comments


@router.get("/user/{owner_id}/post/{post_id}", response_model=List[comment_schemas.Comment])
def get_user_comment_by_post(owner_id: int, post_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)):
    db_user_post_comments = comment_dal.get_user_comments_by_post(
        db=db, user_id=owner_id, post_id=post_id, skip=skip, limit=limit)
    return db_user_post_comments


@router.get("/{comment_id}", response_model=comment_schemas.Comment)
def get_comment(comment_id: int, db: Session = Depends(dependencies.get_db)):
    db_comment = comment_dal.get_comment(db=db, comment_id=comment_id)
    return db_comment

# Not implemented
# update
# delete
