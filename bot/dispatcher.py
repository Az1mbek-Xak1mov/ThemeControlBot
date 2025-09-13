from aiogram import Dispatcher, Bot
from environment.utils import Env

dp = Dispatcher()
TOKEN=Env().bot.TOKEN
bot = Bot(token=TOKEN)
