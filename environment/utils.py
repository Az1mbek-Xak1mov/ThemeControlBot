from os import getenv
from dotenv import load_dotenv
load_dotenv()
class Bot:
    TOKEN = getenv("TOKEN")
    SUMMARY_TOKEN = getenv("SUMMARY_TOKEN")
    ADMIN_CHAT_ID=getenv("ADMIN_CHAT_ID")
class DB:
    DB_NAME = getenv("DB_NAME")
    DB_USER = getenv("DB_USER")
    DB_PASSWORD = getenv("DB_PASSWORD")
    DB_HOST = getenv("DB_HOST")
    DB_PORT = getenv("DB_PORT")
class Env:
    bot = Bot()
    db = DB()