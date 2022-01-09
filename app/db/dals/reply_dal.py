from sqlalchemy.orm import Session

from db.models import comment_model

from schemas import comment_schemas


def create_reply(db: Session, reply: comment_schemas.ReplyCreate):
    db_reply = comment_model.Comment(comment=reply.reply)
    db_reply.parent_id = reply.parent_id
    db_reply.post_id = reply.post_id
    db_reply.owner_id = reply.owner_id
    db.add(db_reply)
    db.commit()
    db.refresh(db_reply)
    return db_reply


def get_replies_by_comment(db: Session, comment_id: int, skip: int = 0, limit: int = 100):
    return db.query(comment_model.Comment).filter(comment_model.Comment.parent_id == comment_id).order_by(comment_model.Comment.created_on.desc()).offset(skip).limit(limit).all()
