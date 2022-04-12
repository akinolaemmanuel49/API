import re
import datetime

from pydantic import BaseModel, EmailStr, validator


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    email: EmailStr
    password: str
    confirm_password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "johndoe@mail.com",
                "password": "password",
                "confirm_password": "password",
            }
        }

    @validator("password")
    def check_password(cls, v, values):
        if 'password' in values and 'confirm_password' in values:
            if values['password'] != values['confirm_password']:
                raise ValueError("Passwords don't match")
        return v

    @validator("email")
    def check_email(cls, v):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if (re.fullmatch(regex, v) is None):
            raise ValueError("Invalid email.")
        return v

    @validator("password")
    def check_password_length(cls, v, values):
        if 'password' in values:
            if len(values['password']) < 8:
                raise ValueError(
                    "Password must be at least 8 characters long.")
        return v

    @validator("username")
    def check_username_length(cls, v):
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters long.")
        return v

    @validator("username")
    def check_username(cls, v):
        regex = r'^[A-Za-z_][A-Za-z0-9._]{3,}'
        if (re.fullmatch(regex, v) is None):
            raise ValueError("Invalid email.")
        return v


class UserUpdate(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "johndoe@mail.com",
                "password": "password",
                "confirm_password": "password",
            }
        }

    @validator("password")
    def check_password(cls, v, values):
        if 'password' in values and 'confirm_password' in values:
            if values['password'] != values['confirm_password']:
                raise ValueError("Passwords don't match")
        return v

    @validator("email")
    def check_email(cls, v):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if (re.fullmatch(regex, v) is None):
            raise ValueError("Invalid email.")
        return v

    @validator("password")
    def check_password_length(cls, v, values):
        if 'password' in values:
            if len(values['password']) < 8:
                raise ValueError(
                    "Password must be at least 8 characters long.")
        return v


class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    active: bool
    is_admin: bool
    created: datetime.datetime
    last_modified: datetime.datetime

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 0,
                "username": "johndoe",
                "email": "johndoe@mail.com",
                "active": True,
                "is_admin": False,
                "created": datetime.datetime.utcnow(),
                "last_modified": datetime.datetime.utcnow()
            }
        }


class TokenData(BaseModel):
    access_token: str
    refresh_token: str
    username: str


class Credentials(BaseModel):
    username: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "password": "password",
            }
        }
