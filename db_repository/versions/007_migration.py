from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('nickname', String(length=64)),
    Column('email', String(length=128)),
    Column('role', SmallInteger, default=ColumnDefault(0)),
    Column('password_salt', String(length=16)),
    Column('password_digest', String(length=128)),
    Column('last_login', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['password_digest'].create()
    post_meta.tables['user'].columns['password_salt'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['password_digest'].drop()
    post_meta.tables['user'].columns['password_salt'].drop()
