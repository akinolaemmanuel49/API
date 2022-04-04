from sqlalchemy.orm import Session

from api.v1.db.models import user_model

from api.v1.schemas import user_schemas
from api.v1.authentication import Authentication

auth_handler = Authentication()


def create_user(db: Session, user: user_schemas.UserCreate):
    hashed_password = auth_handler.encode_password(
        plain_password=user.password)
    try:
        db_user = user_model.User(username=user.username,
                                  email=user.email, hashed_password=hashed_password)

        db.add(db_user)
        db.flush()
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()


def get_user(db: Session, user_id: int):
    user = db.query(user_model.User).filter(
        user_model.User.id == user_id).first()
    if user:
        return user
    return None


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(user_model.User).order_by(user_model.User.created.desc()).offset(skip).limit(limit).all()


def get_user_by_username(db: Session, username: str):
    return db.query(user_model.User).filter(user_model.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(user_model.User).filter(user_model.User.email == email).first()


def update_user(db: Session, user: user_schemas.UserUpdate, username: str):
    db_user = db.query(user_model.User).filter(
        user_model.User.username == username).first()
    if user:
        try:
            db_user.email = user.email
            db_user.hashed_password = auth_handler.encode_password(
                plain_password=user.password)
            db.commit()
        except Exception as e:
            db.rollback()
    return db_user


def delete_user(db: Session, user: user_model.User):
    user = db.query(user_model.User).filter(
        user_model.User.id == user.id).first()
    if user:
        try:
            db.delete(user)
            db.commit()
        except Exception as e:
            db.rollback()
