import datetime
import uuid

from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from ..config import Base
from .post_model import Post
from .comment_model import Comment


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    active = Column(Boolean, index=True, default=True, nullable=False)
    is_admin = Column(Boolean, index=True, default=False, nullable=False)

    posts = relationship("Post", back_populates="owner",
                         cascade="all, delete-orphan")
    comments = relationship(
        "Comment", back_populates="owner", cascade="all, delete-orphan")
    # profile = relationship("Profile", back_populates="owner")

    created = Column(
        DateTime, default=lambda: datetime.datetime.utcnow(), index=True, nullable=False)
    last_modified = Column(DateTime, default=lambda: datetime.datetime.utcnow(
    ), onupdate=datetime.datetime.utcnow(), index=True, nullable=False)

    def serializer(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "active": self.active,
            "is_admin": self.is_admin,
            "created": self.created,
            "last_modified": self.last_modified,
        }

    def __repr__(self):
        return "<User(username='{}')>".format(self.username)
