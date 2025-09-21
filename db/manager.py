import datetime

from sqlalchemy import select, insert, func, update, desc
from sqlalchemy.orm import sessionmaker, Session
from db.engine import engine
from db.models import User, Group, group_user, Theme

SessionLocal: sessionmaker = sessionmaker(bind=engine)
session: Session = SessionLocal()
from sqlalchemy.dialects.postgresql import insert as pg_insert


async def select_group(chat_id: int) -> Group | None:
    return session.execute(
        select(Group).where(Group.chat_id == chat_id)
    ).scalars().first()

async def select_group_users(user_chat_id: int) -> list[dict]:
    stmt = (
            select(Group.chat_id, Group.title)
            .join(group_user, group_user.c.group_chat_id == Group.chat_id)
            .where(group_user.c.user_chat_id == user_chat_id)
        )
    result = session.execute(stmt)
    rows = result.fetchall()
    return [row.title for row in rows]

async def save_group(chat_id: int, title: str) -> Group:
    grp = select_group(chat_id)
    if grp:
        if grp.title != title:
            grp.title = title
            session.commit()
        return grp

    stmt = insert(Group).values(chat_id=chat_id, title=title)
    session.execute(stmt)
    session.commit()
    return select_group(chat_id)



async def select_one(user_chat_id: int) -> User | None:
    return session.execute(
        select(User).where(User.chat_id == user_chat_id)
    ).scalars().first()


async def save_user(values: dict) -> User:
    existing = select_one(values["chat_id"])
    if existing:
        return existing
    stmt = insert(User).values(**values)
    session.execute(stmt)
    session.commit()
    return select_one(values["chat_id"])


async def select_lang(chat_id: int) -> str | None:
    enum_val = session.execute(
        select(User.lang).where(User.chat_id == chat_id)
    ).scalars().first()
    return enum_val.value if enum_val else None


async def save_theme(values: dict):
    stmt = insert(Theme).values(**values)
    session.execute(stmt)
    session.commit()
    return

async def get_ongoing_theme(chat_id: int) -> str | None:
    stmt = select(Theme).where(Theme.chat_id == chat_id, Theme.status == 'ongoing')\
                        .order_by(Theme.created_at.desc()).limit(1)
    result = session.execute(stmt).scalars().first()
    return result.title if result is not None else None

async def set_theme_done(chat_id: int):
    stmt = (
        update(Theme)
        .where(Theme.chat_id == chat_id, Theme.status == 'ongoing')
        .values(status='done')
    )
    res = session.execute(stmt)
    session.commit()
    return res.rowcount


async def update_lang(chat_id: int, lang: str) -> None:
    stmt = (
        update(User)
        .where(User.chat_id == chat_id)
        .values(lang=lang)
    )
    session.execute(stmt)
    session.commit()

async def add_user_to_group(user_chat_id: int, group_chat_id: int):
    stmt = pg_insert(group_user).values(
        group_chat_id=group_chat_id,
        user_chat_id=user_chat_id
    ).on_conflict_do_nothing(
        index_elements=['group_chat_id', 'user_chat_id']
    )
    session.execute(stmt)
    session.commit()

async def get_all_group_chat_ids_async():
    result = session.execute(select(Group.chat_id))
    return result.scalars().all()
