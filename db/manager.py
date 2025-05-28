import datetime

from sqlalchemy import select, insert, func
from sqlalchemy.orm import sessionmaker, Session
from db.engine import engine
from db.models import User, Message, Group, group_user

# Create a scoped session
SessionLocal: sessionmaker = sessionmaker(bind=engine)
session: Session = SessionLocal()
from sqlalchemy.dialects.postgresql import insert as pg_insert


# ─── GROUPS ────────────────────────────────────────────────────────────────

async def get_all_groups() -> list[Group]:
    return session.execute(select(Group)).scalars().all()


async def select_group(chat_id: int) -> Group | None:
    return session.execute(
        select(Group).where(Group.chat_id == chat_id)
    ).scalars().first()


async def save_group(chat_id: int, title: str) -> Group:
    grp = await select_group(chat_id)
    if grp:
        if grp.title != title:
            grp.title = title
            session.commit()
        return grp

    stmt = insert(Group).values(chat_id=chat_id, title=title)
    session.execute(stmt)
    session.commit()
    return await select_group(chat_id)


# ─── USERS ─────────────────────────────────────────────────────────────────

async def get_all_users() -> list[User]:
    return session.execute(select(User)).scalars().all()


async def select_one(user_chat_id: int) -> User | None:
    return session.execute(
        select(User).where(User.chat_id == user_chat_id)
    ).scalars().first()


async def save_user(values: dict) -> User:
    existing = await select_one(values["chat_id"])
    if existing:
        return existing
    stmt = insert(User).values(**values)
    session.execute(stmt)
    session.commit()
    return await select_one(values["chat_id"])


# ─── MESSAGES ───────────────────────────────────────────────────────────────

async def save_message(values: dict):
    text = values.get("messages", "")
    if len(text) <= 3:
        return
    stmt = insert(Message).values(**values)
    session.execute(stmt)
    session.commit()


async def get_messages_for_group(
        group: Group,
        days: int
) -> list[Message]:
    return await get_messages_for_chat(group.chat_id, days)


# ─── GROUP–USER LINK ────────────────────────────────────────────────────────

async def get_users_in_group(group: Group) -> list[User]:
    return group.users


async def add_user_to_group(
        user_chat_id: int,
        group_chat_id: int
):
    stmt = pg_insert(group_user).values(
        group_chat_id=group_chat_id,
        user_chat_id=user_chat_id
    ).on_conflict_do_nothing(
        index_elements=["group_chat_id", "user_chat_id"]
    )

    session.execute(stmt)
    session.commit()


async def get_user_objects_for_group(group_chat_id: int) -> list[User]:
    stmt = (
        select(User)
        .select_from(group_user.join(
            User, User.chat_id == group_user.c.user_chat_id
        ))
        .where(group_user.c.group_chat_id == group_chat_id)
    )
    return session.execute(stmt).scalars().all()


async def total_messages(from_date, group_chat_id):
    now = datetime.datetime.now()
    date_from = now - datetime.timedelta(days=from_date)
    query = select(func.count(Message.id)).where(Message.created_at > date_from, Message.chat_id == group_chat_id)
    result = session.execute(query)
    return result.scalar()


async def get_messages_for_chat(from_date, group_chat_id, user_chat_id) -> list[Message]:
    now = datetime.datetime.now()
    date_from = now - datetime.timedelta(days=from_date)
    query = select(func.count(Message.id)).where(Message.created_at > date_from, Message.chat_id == group_chat_id,
                                                 Message.user_id == user_chat_id)
    result = session.execute(query)
    return result.scalar()



##################################33