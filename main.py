import logging
import asyncio
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
import sys
from aiogram.enums import ParseMode
from aiogram.utils.i18n import I18n, FSMI18nMiddleware
from bot.dispatcher import TOKEN
from bot.handler import *
from db.creating_db import create_database


async def main() -> None:
    i18n = I18n(path='locales', default_locale='en' , domain='messages')
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.update.middleware.register(FSMI18nMiddleware(i18n))
    await dp.start_polling(bot)


if __name__ == "__main__":
    create_database()
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
