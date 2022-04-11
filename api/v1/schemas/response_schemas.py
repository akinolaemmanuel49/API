from typing import Any, List, Optional
from pydantic import BaseModel
from fastapi import status

from api.v1.schemas.user_schemas import User


class ResponseBase(BaseModel):
    pass


class ResponseCreateUser(ResponseBase):
    data: User
    message: str = "Success"
    code: int = status.HTTP_201_CREATED


class ResponseSingleUserQuery(ResponseBase):
    data: User
    message: str = "Success"
    code: int = status.HTTP_200_OK


class ResponseMultipleUsersQuery(ResponseBase):
    data: List[User]
    message: str = "Success"
    count: int
    code: int = status.HTTP_200_OK


class ResponseSuccess(ResponseBase):
    message: Optional[str] = None
    code: int = status.HTTP_200_OK


class ResponseError(ResponseBase):
    message: Optional[str] = None
    code: int
