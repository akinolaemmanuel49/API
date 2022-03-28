"""
This handles routes pertaining to creating, modiifying, logging in a user."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app import dependencies

from app.db.dals.user_dal import auth_handler
from app.db.dals import user_dal

from app.schemas import user_schemas

security = HTTPBearer()

router = APIRouter(prefix="/users", tags=['Users'])


@router.post("/", response_model=user_schemas.User)
def create_user(user: user_schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
    db_user = user_dal.get_user_by_username(db=db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400, detail="Email is already registered")
    return user_dal.create_user(db=db, user=user)


@router.get("/refresh_token")
def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    refresh_token = credentials.credentials
    new_token = auth_handler.refresh_token(refresh_token)
    return {"access_token": new_token}


@router.get("/", response_model=List[user_schemas.User])
def get_users(db: Session = Depends(dependencies.get_db), skip: int = 0, limit: int = 100):
    db_users = user_dal.get_users(db, skip=skip, limit=limit)
    return db_users


@router.get("/user", response_model=user_schemas.User)
def get_user(id: Optional[int] = None, email: Optional[str] = None, username: Optional[str] = None, db: Session = Depends(dependencies.get_db)):
    if id is not None:
        db_user = user_dal.get_user(db=db, user_id=id)
    elif email is not None:
        db_user = user_dal.get_user_by_email(db=db, email=email)
    elif username is not None:
        db_user = user_dal.get_user_by_username(db=db, username=username)
    else:
        raise HTTPException(
            status_code=400, detail="Must provide either id or email")
    return db_user


@router.post("/login", response_model=user_schemas.TokenData)
def login(credentials: user_schemas.Credentials, db: Session = Depends(dependencies.get_db)):
    db_user = user_dal.get_user_by_username(
        db=db, username=credentials.username)
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect username")
    if not auth_handler.decode_password(credentials.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    access_token = auth_handler.encode_token(db_user.id)
    refresh_token = auth_handler.encode_refresh_token(db_user.id)
    user_id = auth_handler.decode_token(access_token)
    return {"access_token": access_token, "refresh_token": refresh_token, "user_id": user_id}
