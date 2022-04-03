"""
This handles routes pertaining to creating, modiifying, logging in a user."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import EmailStr, ValidationError
from sqlalchemy.orm import Session

from api.v1 import dependencies

from api.v1.db.dals.user_dal import auth_handler
from api.v1.db.dals import user_dal

from api.v1.schemas import user_schemas

security = HTTPBearer()

router = APIRouter(prefix="/users", tags=['Users'])


@router.post("/", response_model=user_schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: user_schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
    check_username = user_dal.get_user_by_username(
        db=db, username=user.username)
    if check_username:
        if check_username.username == str(user.username):
            raise HTTPException(
                status_code=400, detail="This username is already taken.")
    check_email = user_dal.get_user_by_email(db=db, email=user.email)
    if check_email:
        if check_email.email == str(user.email):
            raise HTTPException(
                status_code=400, detail="Email is already registered.")
    try:
        new_user = user_dal.create_user(db=db, user=user)
        return new_user
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


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
def get_user(id: Optional[int] = None, email: Optional[EmailStr] = None, username: Optional[str] = None, db: Session = Depends(dependencies.get_db)):
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


@router.delete("/", response_model=user_schemas.User)
def delete_user(id: Optional[int], email: Optional[EmailStr] = None, username: Optional[str] = None, db: Session = Depends(dependencies.get_db)):
    if id is not None:
        db_user = user_dal.get_user(db=db, user_id=id)
        if db_user:
            user_dal.delete_user(db=db, user=db_user)
    elif email is not None:
        db_user = user_dal.get_user_by_email(db=db, email=email)
        if db_user:
            user_dal.delete_user(db=db, user=db_user)
    elif username is not None:
        db_user = user_dal.get_user_by_username(db=db, username=username)
        if db_user:
            user_dal.delete_user(db=db, user=db_user)
    else:
        raise HTTPException(
            status_code=400, detail="Must provide either id or email")
    return db_user