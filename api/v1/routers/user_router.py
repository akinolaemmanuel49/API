"""
This handles routes pertaining to creating, modiifying, logging in a user.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import EmailStr, ValidationError
from sqlalchemy.orm import Session

from api.v1 import dependencies

from api.v1.db.dals.user_dal import auth_handler
from api.v1.db.dals import user_dal

from api.v1.schemas import user_schemas, response_schemas

security = HTTPBearer()

router = APIRouter(prefix="/users", tags=['Users'])


@router.post("/", response_model=response_schemas.ResponseCreateUser, status_code=status.HTTP_201_CREATED)
def create_user(user: user_schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
    check_username = user_dal.get_user_by_username(
        db=db, username=user.username)
    if check_username:
        if check_username.username == user.username:
            raise HTTPException(
                status_code=400, detail="This username is already taken.")
    check_email = user_dal.get_user_by_email(db=db, email=user.email)
    if check_email:
        if check_email.email == user.email:
            raise HTTPException(
                status_code=400, detail="Email is already registered.")
    try:
        new_user = user_dal.create_user(db=db, user=user)
        return response_schemas.ResponseCreateUser(data=new_user)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/refresh_token")
def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    refresh_token = credentials.credentials
    new_token = auth_handler.refresh_token(refresh_token)
    return {"access_token": new_token}


@router.get("/", response_model=response_schemas.ResponseMultipleUsersQuery)
def get_users(db: Session = Depends(dependencies.get_db), skip: int = 0, limit: int = 100):
    db_users = user_dal.get_users(db, skip=skip, limit=limit)
    return response_schemas.ResponseMultipleUsersQuery(data=db_users, count=len(db_users))


@router.get("/user", response_model=response_schemas.ResponseSingleUserQuery, responses={status.HTTP_400_BAD_REQUEST: {'model': response_schemas.ResponseError, 'description': 'Error: Bad request'}, status.HTTP_404_NOT_FOUND: {'model': response_schemas.ResponseError, 'description': 'Error: User not found'}})
def get_user(id: Optional[int] = None, username: Optional[str] = None, email: Optional[EmailStr] = None, db: Session = Depends(dependencies.get_db)):
    if id is not None:
        db_user = user_dal.get_user_by_id(db=db, id=id)
        if db_user:
            user_dal.delete_user(db=db, user=db_user)

    if username is not None:
        db_user = user_dal.get_user_by_username(db=db, username=username)
        if db_user:
            user_dal.delete_user(db=db, user=db_user)

    if email is not None:
        db_user = user_dal.get_user_by_email(db=db, email=email)
        if db_user:
            user_dal.delete_user(db=db, user=db_user)

    if id == None and username == None and email == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=jsonable_encoder(
            response_schemas.ResponseError(message="No user id, username or email provided", code=status.HTTP_400_BAD_REQUEST)))

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=jsonable_encoder(response_schemas.ResponseError(message="User not found", code=status.HTTP_404_NOT_FOUND)))
    return response_schemas.ResponseSingleUserQuery(data=db_user)


@router.post("/login", response_model=user_schemas.TokenData)
def login(credentials: user_schemas.Credentials, db: Session = Depends(dependencies.get_db)):
    db_user = user_dal.get_user_by_username(
        db=db, username=credentials.username)
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect username")
    if not auth_handler.decode_password(credentials.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    access_token = auth_handler.encode_token(db_user.username)
    refresh_token = auth_handler.encode_refresh_token(db_user.username)
    username = auth_handler.decode_token(access_token)
    return user_schemas.TokenData(access_token=access_token, refresh_token=refresh_token, username=username)


@router.put("/user", response_model=response_schemas.ResponseSingleUserQuery, responses={status.HTTP_400_BAD_REQUEST: {'model': response_schemas.ResponseError, 'description': 'Error: Bad request'}, status.HTTP_404_NOT_FOUND: {'model': response_schemas.ResponseError, 'description': 'Error: User not found'}, status.HTTP_401_UNAUTHORIZED: {'model': response_schemas.ResponseError, 'description': 'Error: Unauthorized'}})
def update_user(user: user_schemas.UserUpdate, credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(dependencies.get_db)):
    access_token = credentials.credentials
    username = auth_handler.decode_token(access_token)
    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=jsonable_encoder(response_schemas.ResponseError(
            message="User is not authorized.", code=status.HTTP_401_UNAUTHORIZED)))
    db_user = user_dal.get_user_by_username(db=db, username=username)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=jsonable_encoder(response_schemas.ResponseError(
            message="User not found.", code=status.HTTP_404_NOT_FOUND)))
    try:
        updated_user = user_dal.update_user(
            db=db, user=user, username=username)
        return response_schemas.ResponseSingleUserQuery(data=updated_user)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=jsonable_encoder(
            response_schemas.ResponseError(message=str(e), code=status.HTTP_400_BAD_REQUEST)))


@router.delete("/", response_model=response_schemas.ResponseSuccess, status_code=status.HTTP_200_OK,
               responses={
                   status.HTTP_404_NOT_FOUND: {"model": response_schemas.ResponseError, "description": "Error: Not Found."},
                   status.HTTP_400_BAD_REQUEST: {
                       "model": response_schemas.ResponseError, "description": "Error: Bad Request."}
               },)
def delete_user(id: Optional[int] = None, username: Optional[str] = None, email: Optional[EmailStr] = None, db: Session = Depends(dependencies.get_db)):
    if id is not None:
        db_user = user_dal.get_user_by_id(db=db, id=id)
        if db_user:
            user_dal.delete_user(db=db, user=db_user)

    if username is not None:
        db_user = user_dal.get_user_by_username(db=db, username=username)
        if db_user:
            user_dal.delete_user(db=db, user=db_user)

    if email is not None:
        db_user = user_dal.get_user_by_email(db=db, email=email)
        if db_user:
            user_dal.delete_user(db=db, user=db_user)

    if id == None and username == None and email == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=jsonable_encoder(
            response_schemas.ResponseError(message="Must provide an id, username or email.", code=status.HTTP_400_BAD_REQUEST)))

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=jsonable_encoder(response_schemas.ResponseError(message="User not found.")))
    return response_schemas.ResponseSuccess(message="User was successfully deleted.", code=status.HTTP_404_NOT_FOUND)
