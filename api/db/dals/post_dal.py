from sqlalchemy.orm import Session

from api.v1.db.models import post_model

from api.v1.schemas import post_schemas


def create_post(db: Session, owner_id: int, post: post_schemas.PostCreate):
    db_post = post_model.Post(post=post.post)
    db_post.owner_id = owner_id
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_user_posts(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(post_model.Post).filter(post_model.Post.owner_id == user_id).order_by(post_model.Post.created.desc()).offset(skip).limit(limit).all()


def get_all_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(post_model.Post).order_by(post_model.Post.created.desc()).offset(skip).limit(limit).all()


def get_user_post(db: Session, user_id: int, post_id: int):
    return db.query(post_model.Post).filter(post_model.Post.owner_id == user_id, post_model.Post.id == post_id).first()


def get_a_post(db: Session, post_id: int):
    return db.query(post_model.Post).filter(post_model.Post.id == post_id).first()


def update_post(db: Session, post_id: int, user_id: int, post: post_schemas.PostUpdate):
    db_post = db.query(post_model.Post).filter(
        post_model.Post.id == post_id, post_model.Post.owner_id == user_id).first()
    db_post.post = post.post
    db.commit()
    return db_post


def delete_post(db: Session, post_id: int, user_id: int):
    db_post = db.query(post_model.Post).filter(post_model.Post.id ==
                                               post_id, post_model.Post.owner_id == user_id).first()
    db.delete(db_post)
    db.commit()
    return db_post
