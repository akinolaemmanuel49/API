from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta = MetaData(bind=migrate_engine)
    users = Table('users', meta, autoload=True)
    is_admin = Column('is_admin', Boolean, default=False)
    is_admin.create(users)


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta = MetaData(bind=migrate_engine)
    users = Table('users', meta, autoload=True)
    users.c.is_admin.drop()
