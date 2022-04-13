import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from ..config import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="posts")
    comments = relationship(
        "Comment", back_populates="post", cascade="all, delete-orphan")

    created = Column(DateTime, default=lambda: datetime.datetime.utcnow())
    last_modified = Column(DateTime, default=lambda: datetime.datetime.utcnow(
    ), onupdate=datetime.datetime.utcnow())

    def serializer(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "owner_id": self.owner_id,
            "created": self.created,
            "last_modified": self.last_modified
        }

    def __repr__(self) -> str:
        return "<Post(title='{}', owner_id='{}')>".format(self.title, self.owner_id)
