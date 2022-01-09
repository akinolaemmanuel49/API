from sqlalchemy.orm import Session

from db.models import user_model

from schemas import user_schemas
import authentication


def create_user(db: Session, user: user_schemas.UserCreate):
    hashed_password = authentication.Authentication.encode_password(
        user.password)
    db_user = user_model.User(username=user.username,
                              email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    user = db.query(user_model.User).filter(
        user_model.User.id == user_id).first()
    if user:
        return user
    return None


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(user_model.User).order_by(user_model.User.created_on.desc()).offset(skip).limit(limit).all()


def get_user_by_username(db: Session, username: str):
    return db.query(user_model.User).filter(user_model.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(user_model.User).filter(user_model.User.email == email).first()
