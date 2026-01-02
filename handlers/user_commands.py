from pytz import timezone
from datetime import datetime

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery

from database.db import db
from utils.json_utils import get_lanuage_msg
from keyboards.inline.user import get_main_menu, get_language_selection_keyboard

router = Router()


@router.message(F.text == "/start")
async def start_func(msg: Message, bot: Bot):
    user_id = msg.from_user.id
    username = msg.from_user.username or None
    first_name = msg.from_user.first_name
    now_date = datetime.now(timezone("Europe/Kyiv")).strftime("%Y.%m.%d")

    user_info = await db.get_user(user_id)
    if user_info is None:
        await db.create_user(
            user_id=user_id, first_name=first_name, username=username, reg_date=now_date
        )
        await db.add_user_levels(user_id)
        await msg.answer(
            f"Hello, firstly, pick your language \n\nПривіт, спочатку оберіть вашу мову",
            reply_markup=await get_language_selection_keyboard(),
        )
        return

    else:
        await db.updated_username(user_id, username)

    await bot.send_message(
        chat_id=msg.from_user.id,
        text=f"👋 Привет, <b>{msg.from_user.full_name}</b>",
        reply_markup=await get_main_menu(),
        parse_mode="html",
    )


@router.callback_query(F.data.startswith("set_lang_"))
async def set_language_callback(call: CallbackQuery, bot: Bot):
    user_id = call.from_user.id
    selected_language = call.data.split("set_lang_")[1]

    msg_text = await get_lanuage_msg(selected_language, "hello")

    await bot.edit_message_text(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        text=f"{msg_text}, <b>{call.from_user.full_name}</b>",
        reply_markup=await get_main_menu(),
        parse_mode="html",
    )

    await db.update_language(user_id, selected_language)
