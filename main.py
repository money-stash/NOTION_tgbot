import asyncio
from aiogram import Bot, Dispatcher

from pytz import timezone
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from routers import routers

from utils.scheduler import scheduled_task
from utils.bot_commands import set_commands
from utils.remainders import shchedule_daily_remainders

from database.db import db
from config import TOKEN


async def main():
    await db.init_models()

    bot = Bot(TOKEN)
    dp = Dispatcher()

    dp.include_routers(*routers)

    kyiv_tz = timezone("Europe/Kyiv")

    scheduler = AsyncIOScheduler(timezone=kyiv_tz)
    scheduler.add_job(
        scheduled_task, CronTrigger(hour=0, minute=0, timezone=kyiv_tz), args=[bot]
    )
    scheduler.add_job(
        db.back_daily_to_history, CronTrigger(hour=0, minute=33, timezone=kyiv_tz)
    )
    scheduler.add_job(
        shchedule_daily_remainders,
        CronTrigger(hour=12, minute=0, timezone=kyiv_tz),
        args=[bot],
    )
    scheduler.add_job(
        shchedule_daily_remainders,
        CronTrigger(hour=17, minute=0, timezone=kyiv_tz),
        args=[bot],
    )
    scheduler.add_job(
        shchedule_daily_remainders,
        CronTrigger(hour=22, minute=0, timezone=kyiv_tz),
        args=[bot],
    )
    scheduler.start()

    await bot.delete_webhook(drop_pending_updates=True)
    await set_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
