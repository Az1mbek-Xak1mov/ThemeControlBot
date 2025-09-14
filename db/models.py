import enum

from sqlalchemy import (
    Column,
    BigInteger,
    DateTime,
    ForeignKey,
    Text,
    Table, Enum, text,
)
from sqlalchemy.orm import relationship

from db.engine import Base

group_user = Table(
    'group_users',
    Base.metadata,
    Column(
        'group_chat_id',
        BigInteger,
        ForeignKey('tg_groups.chat_id', ondelete="CASCADE"),
        primary_key=True
    ),
    Column(
        'user_chat_id',
        BigInteger,
        ForeignKey('users.chat_id', ondelete="CASCADE"),
        primary_key=True
    )
)

class User(Base):
    class LanguageEnum(enum.Enum):
        uz = "uz"
        ru = "ru"
    __tablename__ = 'users'
    id       = Column(BigInteger, primary_key=True, autoincrement=True)
    chat_id  = Column(BigInteger, unique=True, nullable=False)
    name     = Column(Text)
    username = Column(Text)
    groups   = relationship('Group', secondary=group_user, back_populates='users')
    lang         = Column(Enum(LanguageEnum), nullable=False, default=LanguageEnum.uz)

class Group(Base):
    __tablename__ = 'tg_groups'
    id      = Column(BigInteger, primary_key=True, autoincrement=True)
    chat_id = Column(BigInteger, unique=True, nullable=False)
    title   = Column(Text, nullable=False)
    users   = relationship('User', secondary=group_user, back_populates='groups')

class Message(Base):
    __tablename__ = 'messages'
    id         = Column(BigInteger, primary_key=True, autoincrement=True)
    chat_id    = Column(BigInteger, nullable=False)
    user_id    = Column(BigInteger, ForeignKey('users.chat_id'))  # point at users.chat_id
    messages   = Column(Text)
    created_at = Column(DateTime)
    user       = relationship('User', backref='messages')

class Theme(Base):
    __tablename__ = 'themes'
    id         = Column(BigInteger, primary_key=True, autoincrement=True)
    chat_id    = Column(BigInteger, nullable=False)
    user_id    = Column(BigInteger, ForeignKey('users.chat_id'))
    title      = Column(Text)
    created_at = Column(DateTime)
    user       = relationship('User', backref='themes')
    status = Column(
        Enum('ongoing', 'done', name='theme_status'),
        nullable=False,
        default='ongoing',
        server_default=text("'ongoing'")
    )