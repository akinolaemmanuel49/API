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


@router.get("/")
def get_user_profiles(db: Session = Depends(dependencies.get_db), skip: int = 0, limit: int = 100):
    db_profiles = profile_dal.get_user_profiles(db=db, skip=skip, limit=limit)
    return db_profiles
