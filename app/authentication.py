import jwt
from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException
from passlib.context import CryptContext

from settings import Settings


class Authentication:
    pwd_context = CryptContext(Settings.ENCRYPTION_SCHEMES)
    secret_key = Settings.JWT_SECRET_KEY

    def encode_password(self, plain_password: str) -> Optional[str]:
        return self.pwd_context.hash(plain_password)

    def decode_password(self, plain_password: str, encoded_password: str) -> bool:
        return self.pwd_context.verify(plain_password, encoded_password)

    def encode_token(self, username: str) -> str:
        payload = {
            "exp": datetime.utcnow() + timedelta(minutes=Settings.JWT_EXPIRATION_MINUTES),
            "iat": datetime.utcnow(),
            "scope": "access_token",
            "sub": username
        }
        return jwt.encode(payload, self.secret_key, algorithm=Settings.JWT_ALGORITHM)

    def decode_token(self, token: str) -> Optional[str]:
        try:
            payload = jwt.decode(token, Settings.JWT_SECRET_KEY, algorithms=[
                                 Settings.JWT_ALGORITHM])
            if (payload["scope"] == "access_token"):
                return payload["sub"]
            raise HTTPException(
                status_code=401, detail="Scope for the token is invalid")
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401, detail="Signature expired. Please log in again.")
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=401, detail="Invalid token. Please log in again.")

    def encode_refresh_token(self, username: str) -> Optional[str]:
        payload = {
            "exp": datetime.utcnow() + timedelta(days=Settings.JWT_REFRESH_EXPIRE_HOURS),
            "iat": datetime.utcnow(),
            "scope": "refresh_token",
            "sub": username
        }
        return jwt.encode(payload, self.secret_key, algorithm=Settings.JWT_ALGORITHM)

    def refresh_token(self, refresh_token):
        try:
            payload = jwt.decode(refresh_token, self.secret_key, algorithms=[
                                 Settings.JWT_ALGORITHM])
            if (payload["scope"] == "refresh_token"):
                username = payload["sub"]
                new_token = self.encode_token(username)
                return new_token
            raise HTTPException(
                status_code=401, detail="Scope for the token is invalid")
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401, detail="Signature expired. Please log in again.")
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=401, detail="Invalid token. Please log in again.")
