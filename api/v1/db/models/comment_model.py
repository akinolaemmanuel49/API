import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from ..config import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    comment = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    parent_id = Column(Integer, ForeignKey("comments.id"))

    owner = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
    parent = relationship("Comment", remote_side=[
                          id], back_populates="replies")
    replies = relationship(
        "Comment", back_populates="parent", cascade="all, delete-orphan")

    created = Column(DateTime, default=lambda: datetime.datetime.utcnow())
    last_modified = Column(DateTime, default=lambda: datetime.datetime.utcnow(
    ), onupdate=datetime.datetime.utcnow())

    def serializer(self):
        return {
            "id": self.id,
            "comment": self.comment,
            "owner_id": self.owner_id,
            "post_id": self.post_id,
            "parent_id": self.parent_id,
            "created": self.created,
            "last_modified": self.last_modified
        }

    def __repr__(self) -> str:
        if self.parent_id == None:
            return "<Comment(comment='{}', post_id='{}', owner_id='{}')>".format(self.comment, self.post_id, self.owner_id)
        else:
            return "<Reply(comment='{}', post_id='{}', owner_id='{}', parent_id='{}')>".format(self.comment, self.post_id, self.owner_id, self.parent_id)
