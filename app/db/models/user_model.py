import datetime

from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from ..config import Base
from .post_model import Post
from .comment_model import Comment


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    active = Column(Boolean, default=True)

    posts = relationship("Post", back_populates="owner")
    comments = relationship("Comment", back_populates="owner")

    created = Column(DateTime, default=lambda: datetime.datetime.utcnow())
    last_modified = Column(DateTime, default=lambda: datetime.datetime.utcnow(
    ), onupdate=datetime.datetime.utcnow())
