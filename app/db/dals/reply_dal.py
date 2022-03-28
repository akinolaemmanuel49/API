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
