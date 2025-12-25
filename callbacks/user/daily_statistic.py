from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from database.db import db
from keyboards.inline.user import get_back_to_daily_menu

router = Router()


@router.callback_query(F.data == "daily_statistic")
async def open_daily_stat(call: CallbackQuery, bot: Bot):
    user_id = call.from_user.id
    daily_stat = await db.get_daily_stat(user_id)
    answ_text = "📊 Статистика ежедневных задач\n\n"

    answ_text += f"📝 Всего задач: {daily_stat['total']}\n"
    answ_text += f"✅ Выполнено: {daily_stat['done']}\n"
    answ_text += f"❌ Не выполнено: {daily_stat['not_done']}\n"

    await bot.edit_message_text(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        text=answ_text,
        reply_markup=await get_back_to_daily_menu(),
    )
