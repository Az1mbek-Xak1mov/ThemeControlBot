import asyncio
import logging
import sys
from os import getenv
from aiogram import Bot, Dispatcher, html, F
from aiogram.client import bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from bot.dispatcher import dp
from db.creating_db import create_database
from db.manager import save_user, save_message, select_one, save_group, add_user_to_group
from db.models import User
from openpyxl import Workbook
import datetime
@dp.message()
async def handle_message(message: Message):
    if message.chat.type in ("group", "supergroup"):
        user_info = {
            "chat_id": message.from_user.id,
            "username": message.from_user.username or "",
            "name": message.from_user.first_name or "",
        }
        if not await select_one(message.from_user.id):
            await save_user(user_info)

    if message.chat.type in ("group", "supergroup"):
        grp = await save_group(message.chat.id, message.chat.title or f"Group {message.chat.id}")
        await add_user_to_group(
            user_chat_id=message.from_user.id,
            group_chat_id=grp.chat_id
        )
    if message.chat.type in ("group", "supergroup"):
        message_info = {
            "user_id": message.from_user.id,
            "chat_id": message.chat.id,
            "messages": message.text,
            "created_at": datetime.datetime.utcnow(),
        }
        await save_message(message_info)

