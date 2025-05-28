from sqlalchemy import Column, BigInteger, Text, Integer, Boolean, DateTime, ForeignKey, create_engine, JSON, Table, \
    String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from db.engine import DB_URL
Base = declarative_base()

group_user = Table(
    'group_user', Base.metadata,
    Column('group_chat_id', BigInteger, ForeignKey('tg_group.chat_id'), primary_key=True),
    Column('user_chat_id',  BigInteger, ForeignKey('user.chat_id'),    primary_key=True)
)

class Group(Base):
    __tablename__ = 'tg_group'
    id = Column(BigInteger, primary_key=True)
    chat_id = Column(BigInteger, unique=True, nullable=False)
    title = Column(String, nullable=False)
    users = relationship('User', secondary=group_user, back_populates='groups')

class User(Base):
    __tablename__ = 'user'
    id        = Column(BigInteger, primary_key=True)
    chat_id   = Column(BigInteger, unique=True, nullable=False)
    name      = Column(String)
    username  = Column(String)
    groups = relationship('Group', secondary=group_user, back_populates='users')

class Message(Base):
    __tablename__ = 'message'
    id         = Column(BigInteger, primary_key=True)
    user_id    = Column(BigInteger, ForeignKey('user.chat_id'))
    chat_id    = Column(BigInteger, ForeignKey('group.chat_id'))
    messages   = Column(String)
    created_at = Column(DateTime)
    user = relationship('User')

engine = create_engine(DB_URL)
Base.metadata.create_all(engine)