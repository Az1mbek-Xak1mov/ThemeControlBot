import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message




admin_chat_id=5430618568
TOKEN="7901827915:AAEr0_cqQLd3dowZrPtXjTbVYGzXJcXZ3JQ"
bot=Bot(TOKEN)
dp = Dispatcher()


@dp.message()
async def name_handler() -> None:
    await bot.send_message(admin_chat_id,'Hello')

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(name_handler())