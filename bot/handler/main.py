from aiogram import F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.i18n import gettext as _
from bot.buttons.reply import make_reply_btn
from bot.dispatcher import dp, bot
from db.manager import select_one, save_user, update_lang, select_group_users, get_all_group_chat_ids_async, \
    add_user_to_group
from aiogram.utils.i18n import lazy_gettext as __

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("Not inside private start")
    if not message.chat.type in ("group", "supergroup"):
        await message.answer("inside private start")
        gids = get_all_group_chat_ids_async()
        for gid in gids:
            member = await bot.get_chat_member(gid, message.from_user.id)
            if member.status in ("member", "administrator", "creator"):
                add_user_to_group(message.from_user.id,gid)
        if not select_one(message.from_user.id):
            user_info = {
                "chat_id": message.from_user.id,
                "username": message.from_user.username or "",
                "name": message.from_user.first_name or "",
            }
            save_user(user_info)
            language_menu = [
                "🇺🇿 O‘zbekcha",
                "🇷🇺 Русский",
            ]
            markup = make_reply_btn(language_menu, sizes=[2])
            await message.answer(_("Tilni tanlang"), reply_markup=markup)
        else:
            await message.answer("inside private start")
            sizes = [2]
            menu = [
                _("👥 Guruhlar"),
                _("🌐 Til"),
            ]
            markup = make_reply_btn(menu, sizes)
            await message.answer(_("Asosiy Menyu"), reply_markup=markup)


@dp.message(F.text == __("🌐 Til"))
async def show_language_menu(message: Message):
    await message.answer("Not inside private til")
    if not message.chat.type in ("group", "supergroup"):
        await message.answer("inside private til")
        language_menu = [
            "🇺🇿 O‘zbekcha",
            "🇷🇺 Русский",
        ]
        markup = make_reply_btn(language_menu, sizes=[2])
        await message.answer(_("🌐 Tilni tanlang"), reply_markup=markup)


@dp.message(F.text.in_(["🇺🇿 O‘zbekcha","🇷🇺 Русский"]))
async def handle_language_choice(message: Message, state: FSMContext, i18n):
    await message.answer("Not inside private choice")
    if not message.chat.type in ("group", "supergroup"):
        await message.answer("inside private choice")
        selected = message.text
        lang_code = "ru" if selected == "🇷🇺 Русский" else "uz"
        update_lang(message.from_user.id, lang_code)
        await state.update_data(locale=lang_code)
        i18n.current_locale = lang_code
        sizes = [2]
        menu = [
            _("👥 Guruhlar"),
            _("🌐 Til"),
        ]
        markup = make_reply_btn(menu, sizes)
        await message.answer(_("Asosiy Menyu"), reply_markup=markup)

@dp.message(F.text == __("👥 Guruhlar"))
async def show_language_menu(message: Message):
    await message.answer("Not inside private gruhlar")
    if not message.chat.type in ("group", "supergroup"):
        await message.answer("inside private gruhlar")
        group_titles = select_group_users(message.chat.id)
        formatted_output = ','.join(group_titles)
        markup = make_reply_btn([_("🔙 Orqaga")], sizes=[1])
        await message.answer(f"{_('👥 Guruhlar')}:{formatted_output}", reply_markup=markup)

@dp.message(F.text==__("🔙 Orqaga"))
async def back_panel(message:Message):
    await message.answer("Not inside private orqaga")
    if not message.chat.type in ("group", "supergroup"):
        await message.answer("inside private orqaga")
        sizes = [2]
        menu = [
            _("👥 Guruhlar"),
            _("🌐 Til"),
        ]
        markup = make_reply_btn(menu, sizes)
        await message.answer(_("Asosiy Menyu"), reply_markup=markup)