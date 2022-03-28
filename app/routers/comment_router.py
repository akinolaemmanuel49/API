from typing import List

from fastapi import APIRouter, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app import dependencies

from app.db.dals import comment_dal
from app.db.dals.user_dal import auth_handler
from app.schemas import comment_schemas

security = HTTPBearer()

router = APIRouter(prefix="/comments", tags=['Comments'])


@router.post("/", response_model=comment_schemas.Comment)
def create_comment(post_id: int, comment: comment_schemas.CommentCreate, db: Session = Depends(dependencies.get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
    access_token = credentials.credentials
    user_id = auth_handler.decode_token(access_token)
    db_comment = comment_dal.create_comment(
        owner_id=user_id, post_id=post_id, db=db, comment=comment)
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


@router.get("/user/post/{post_id}", response_model=List[comment_schemas.Comment])
def get_user_comment_by_post(owner_id: int, post_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)):
    db_user_post_comments = comment_dal.get_user_comments_by_post(
        db=db, user_id=owner_id, post_id=post_id, skip=skip, limit=limit)
    return db_user_post_comments


@router.get("/{comment_id}", response_model=comment_schemas.Comment)
def get_comment(comment_id: int, db: Session = Depends(dependencies.get_db)):
    db_comment = comment_dal.get_comment(db=db, comment_id=comment_id)
    return db_comment


@router.put("/{comment_id}", response_model=comment_schemas.Comment)
def update_comment(comment_id: int, comment: comment_schemas.CommentUpdate, db: Session = Depends(dependencies.get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
    access_token = credentials.credentials
    user_id = auth_handler.decode_token(access_token)
    db_update_comment = comment_dal.update_comment(
        db=db, user_id=user_id, comment_id=comment_id, comment=comment)
    return db_update_comment


@router.delete("/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(dependencies.get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
    access_token = credentials.credentials
    user_id = auth_handler.decode_token(access_token)
    db_delete_comment = comment_dal.delete_comment(
        db=db, owner_id=user_id, comment_id=comment_id)
    return db_delete_comment
