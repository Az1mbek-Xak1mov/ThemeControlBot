from sqlalchemy import (
    Column,
    BigInteger,
    DateTime,
    ForeignKey,
    Text,
    Table,
)
from sqlalchemy.orm import relationship

from db.engine import Base

# Association table for many-to-many relationship between Group and User
group_user = Table(
    'group_user',
    Base.metadata,
    Column('group_chat_id', BigInteger, ForeignKey('tg_group.chat_id', ondelete="CASCADE"), primary_key=True),
    Column('user_chat_id', BigInteger, ForeignKey('user.chat_id', ondelete="CASCADE"), primary_key=True)
)


class User(Base):
    __tablename__ = 'user'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    chat_id = Column(BigInteger, unique=True, nullable=False)
    name = Column(Text)
    username = Column(Text)
    groups = relationship('Group', secondary=group_user, back_populates='users')


class Group(Base):
    __tablename__ = 'tg_group'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    chat_id = Column(BigInteger, unique=True, nullable=False)
    title = Column(Text, nullable=False)
    users = relationship('User', secondary=group_user, back_populates='groups')


class Message(Base):
    __tablename__ = 'message'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    chat_id = Column(BigInteger, nullable=False)  # Not a foreign key to avoid FK constraint in your SQL
    user_id = Column(BigInteger, ForeignKey('user.chat_id'))
    messages = Column(Text)
    created_at = Column(DateTime)
    user = relationship('User', backref='messages')


