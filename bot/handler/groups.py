import datetime
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, BotCommand
from ai.client import check_msg
from bot.dispatcher import dp, bot
from bot.handler.chat_history import append_message_to_file, get_last_n_messages_from_file, delete_history_file
from bot.states import NewThemeStates
from db.manager import save_user, select_one, save_group, add_user_to_group, save_theme, set_theme_done, \
    get_ongoing_theme
import datetime
from aiogram.types import Message, BotCommand
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

async def set_bot_commands():
    await bot.set_my_commands([
        BotCommand("newtheme", "Create a new theme (groups only)"),
        BotCommand("cancel", "Cancel current action"),
    ])


@dp.message(Command(commands=["newtheme"]))
async def cmd_newtheme_group(message: Message, state: FSMContext):
    if message.chat.type in ("group", "supergroup"):
        user_info = {
            "chat_id": message.from_user.id,
            "username": message.from_user.username or "",
            "name": message.from_user.first_name or "",
        }
        if not select_one(message.from_user.id):
            save_user(user_info)
        grp = save_group(message.chat.id, message.chat.title or f"Group {message.chat.id}")
        add_user_to_group(
            user_chat_id=message.from_user.id,
            group_chat_id=grp.chat_id
        )
        delete_history_file(message.chat.id)
        await state.set_state(NewThemeStates.waiting_for_text)


@dp.message(NewThemeStates.waiting_for_text)
async def receive_newtheme_text(message: Message, state: FSMContext):
    if message.chat.type in ("group", "supergroup"):
        theme = {
            "user_id": message.from_user.id,
            "chat_id": message.chat.id,
            "title": message.text,
            "created_at": datetime.datetime.utcnow(),
        }
        save_theme(theme)
        await state.set_state(NewThemeStates.ongoing)


@dp.message(Command(commands=["cancel"]))
async def cancel_newtheme(message: Message, state: FSMContext):
    if message.chat.type in ("group", "supergroup"):
        delete_history_file(message.chat.id)
        await state.clear()
        set_theme_done(message.chat.id)

@dp.message()
async def handle_message(message: Message):
    if message.chat.type in ("group", "supergroup"):
        theme_text = get_ongoing_theme(message.chat.id)
        if not theme_text or message.text.startswith("#out"):
            return
        try:
            prev_msgs = get_last_n_messages_from_file(message.chat.id, n=3)
        except Exception as e:
            prev_msgs = []

        combined_input_lines = [f"Theme:{theme_text}"]
        for pm in prev_msgs:
            combined_input_lines.append(f"Message:{pm}")
        combined_input_lines.append(f"Message:{message.text}")
        combined_input = "\n".join(combined_input_lines)

        try:
            is_off_topic = check_msg(combined_input)
        except Exception as e:
            is_off_topic = 'on'
        if is_off_topic == 'out' and not message.text.startswith("#out"):
            await message.delete()
        else:
            append_message_to_file(message.chat.id, message.text)
            grp = save_group(message.chat.id, message.chat.title or f"Group {message.chat.id}")
            add_user_to_group(
                user_chat_id=message.from_user.id,
                group_chat_id=grp.chat_id
            )

