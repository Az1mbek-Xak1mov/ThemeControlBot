import datetime

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.dispatcher import dp
from bot.states import StepByStepStates
from db.manager import save_user, save_message, select_one, save_group, add_user_to_group
from environment.utils import ADMIN
from tasks.daily_summary import send_summary_to_admin_day
from tasks.month_summary import send_summary_to_admin_month
from tasks.week_summary import send_summary_to_admin_week


@dp.message()
async def handle_message(message: Message,state:FSMContext):
    if message.chat.type not in ("group", "supergroup") and str(message.from_user.id)==str(ADMIN.ADMIN_CHAT_ID):
        if message.text.lower()=="week":
            await send_summary_to_admin_week()
        elif message.text.lower()=="month":
            await send_summary_to_admin_month()
        elif message.text.lower()=="day":
            await send_summary_to_admin_day()
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
