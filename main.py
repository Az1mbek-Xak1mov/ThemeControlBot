import logging
import asyncio
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
import sys
from aiogram.enums import ParseMode
from bot.dispatcher import TOKEN
from bot.handler import *
from db.creating_db import create_database


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    create_database()
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
