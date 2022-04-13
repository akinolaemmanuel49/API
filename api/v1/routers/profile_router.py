from typing import Optional

from fastapi import APIRouter, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from api.v1 import dependencies
from api.v1.db.dals import profile_dal, user_dal
from api.v1.db.models import user_model
from api.v1.schemas import profile_schemas

security = HTTPBearer()

router = APIRouter(prefix="/profiles", tags=['Users', 'Profiles'])


@router.post("/")
def create_user_profile(profile: profile_schemas.ProfileCreate, credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(dependencies.get_db)):
    access_token = credentials.credentials
    username = user_dal.auth_handler.decode_token(access_token)
    user = db.query(user_model.User).filter(
        user_model.User.username == username).first()
    db_profile = profile_dal.create_profile(db=db, user=user, profile=profile)
    return db_profile


@router.get("/profile")
def get_user_profile(profile_id: int, db: Session = Depends(dependencies.get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
    access_token = credentials.credentials
    username = user_dal.auth_handler.decode_token(access_token)
    user = db.query(user_model.User).filter(
        user_model.User.username == username).first()
    db_profile = profile_dal.get_user_profile(
        db=db, user=user, profile_id=profile_id)
    return db_profile


@router.get("/profiles")
def get_user_profiles(db: Session = Depends(dependencies.get_db), skip: int = 0, limit: int = 100, credentials: HTTPAuthorizationCredentials = Security(security)):
    access_token = credentials.credentials
    username = user_dal.auth_handler.decode_token(access_token)
    user = db.query(user_model.User).filter(
        user_model.User.username == username).first()
    db_profiles = profile_dal.get_user_profiles(
        db=db, user=user, skip=skip, limit=limit)
    return db_profiles


@router.put("/")
def update_user_profile(profile_id: int, profile: profile_schemas.ProfileUpdate, credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(dependencies.get_db)):
    access_token = credentials.credentials
    username = user_dal.auth_handler.decode_token(access_token)
    user = db.query(user_model.User).filter(
        user_model.User.username == username).first()
    db_profile = profile_dal.update_profile(
        db=db, profile_id=profile_id, user=user, profile=profile)
    return db_profile


@router.delete("/")
def delete_user_profile(profile_id: int, credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(dependencies.get_db)):
    access_token = credentials.credentials
    username = user_dal.auth_handler.decode_token(access_token)
    user = db.query(user_model.User).filter(
        user_model.User.username == username).first()
    db_profile = profile_dal.delete_profile(
        db=db, profile_id=profile_id, user=user)
    return db_profile
