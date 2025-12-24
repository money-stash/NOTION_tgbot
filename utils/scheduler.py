from aiogram import Bot
from aiogram.types.input_file import FSInputFile

from pytz import timezone
from datetime import datetime

from database.db import db
from config import ADMIN_ID


async def scheduled_task(bot: Bot):
    await db.cleanup_daily_tasks()
    file = FSInputFile("database/database.db")

    now_time_and_date = datetime.now(timezone("Europe/Kyiv")).strftime(
        "%Y.%m.%d %H:%M:%S"
    )

    await bot.send_document(
        chat_id=ADMIN_ID,
        document=file,
        caption=f"🗂️ Бекап от {now_time_and_date}",
    )
