import sqlalchemy
from sqlalchemy.orm import Session

from app.db.models import comment_model

from app.schemas import comment_schemas


def create_reply(owner_id: int, parent_id: int, post_id: int, db: Session, reply: comment_schemas.ReplyCreate):
    db_reply = comment_model.Comment(comment=reply.reply)
    db_reply.parent_id = parent_id
    db_reply.post_id = post_id
    db_reply.owner_id = owner_id
    if db_reply.owner_id is not None:
        db.add(db_reply)
        db.commit()
        db.refresh(db_reply)
        return db_reply
    else:
        raise sqlalchemy.exc.SQLAlchemyError


def get_replies_by_comment(db: Session, comment_id: int, skip: int = 0, limit: int = 100):
    return db.query(comment_model.Comment).filter(comment_model.Comment.parent_id == comment_id).order_by(comment_model.Comment.created.desc()).offset(skip).limit(limit).all()


def get_all_user_replies(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(comment_model.Comment).filter(comment_model.Comment.owner_id == user_id, comment_model.Comment.parent_id != None).order_by(comment_model.Comment.created.desc()).offset(skip).limit(limit).all()


def update_reply(db: Session, user_id: int, reply_id: int, reply: comment_schemas.ReplyUpdate):
    db_reply = db.query(comment_model.Comment).filter(
        comment_model.Comment.id == reply_id, comment_model.Comment.owner_id == user_id, comment_model.Comment.parent_id != None).first()
    db_reply.comment = reply.reply
    db.commit()
    return db_reply


def delete_reply(db: Session, owner_id: int, reply_id: int):
    db_reply = db.query(comment_model.Comment).filter(
        comment_model.Comment.owner_id == owner_id, comment_model.Comment.id == reply_id, comment_model.Comment.parent_id != None).first()
    db.delete(db_reply)
    db.commit()
    return db_reply
