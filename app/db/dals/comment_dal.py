import sqlalchemy
from sqlalchemy.orm import Session

from app.db.models import comment_model

from app.schemas import comment_schemas


def create_comment(owner_id: int, post_id: int, db: Session, comment: comment_schemas.CommentCreate):
    db_comment = comment_model.Comment(comment=comment.comment)
    db_comment.owner_id = owner_id
    db_comment.post_id = post_id
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_comment(db: Session, comment_id: int):
    return db.query(comment_model.Comment).filter(comment_model.Comment.id == comment_id, comment_model.Comment.parent_id == None).first()


def get_comments_by_post(db: Session, post_id: int, skip: int = 0, limit: int = 100):
    return db.query(comment_model.Comment).filter(comment_model.Comment.post_id == post_id, comment_model.Comment.parent_id == None).order_by(comment_model.Comment.created.desc()).offset(skip).limit(limit).all()


def get_all_user_comments(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(comment_model.Comment).filter(comment_model.Comment.owner_id == user_id, comment_model.Comment.parent_id == None).order_by(comment_model.Comment.created.desc()).offset(skip).limit(limit).all()


def get_user_comments_by_post(db: Session, user_id: int, post_id: int, skip: int = 0, limit: int = 100):
    return db.query(comment_model.Comment).filter(comment_model.Comment.owner_id == user_id, comment_model.Comment.post_id == post_id, comment_model.Comment.parent_id == None).order_by(comment_model.Comment.created.desc()).offset(skip).limit(limit).all()


def update_comment(db: Session, user_id: int, comment_id: int, comment: comment_schemas.CommentUpdate):
    db_comment = db.query(comment_model.Comment).filter(
        comment_model.Comment.id == comment_id, comment_model.Comment.owner_id == user_id, comment_model.Comment.parent_id == None).first()
    db_comment.comment = comment.comment
    db.commit()
    return db_comment


def delete_comment(db: Session, owner_id: int, comment_id: int):
    db_comment = db.query(comment_model.Comment).filter(
        comment_model.Comment.owner_id == owner_id, comment_model.Comment.id == comment_id, comment_model.Comment.parent_id == None).first()
    db.delete(db_comment)
    db.commit()
    return db_comment
