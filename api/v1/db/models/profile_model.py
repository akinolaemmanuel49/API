import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Date
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM

from ..config import Base


profile_types = ENUM('business', 'personal',
                     name='profile_types', metadata=Base.metadata)


class Profile(Base):

    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=True, default=None)
    last_name = Column(String, nullable=True, default=None)
    date_of_birth = Column(Date, nullable=True, default=None)
    profile_image = Column(String, nullable=True, default=None)
    profile_type = Column('profile_types', profile_types, default='personal')
    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("User", back_populates="profile")

    created = Column(
        DateTime, default=lambda: datetime.datetime.utcnow(), index=True, nullable=False)
    last_modified = Column(DateTime, default=lambda: datetime.datetime.utcnow(
    ), onupdate=datetime.datetime.utcnow(), index=True, nullable=False)

    def serializer(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "profile_image": self.profile_image,
            "profile_type": self.profile_type,
            "created": self.created,
            "last_modified": self.last_modified,
        }

    def __repr__(self):
        return "<Profile(first_name='{}', last_name='{}')>".format(
            self.first_name, self.last_name)
