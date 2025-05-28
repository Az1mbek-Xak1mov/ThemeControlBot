import logging
import asyncio

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
import sys

from aiogram.enums import ParseMode

from bot.dispatcher import TOKEN
from bot.handler import *
from db.manager import db


async def on_startup():
    try:
        await db.create_all()
    except Exception as e:
        logging.exception("Failed to create tables")
        raise


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
