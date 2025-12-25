from handlers import user_commands
from callbacks.user import (
    open_profile,
    back_to_main,
    set_done_daily,
    add_daily_task,
    open_daily_tasks,
    remove_daily_task,
    daily_ok,
    daily_statistic,
)


routers = [
    user_commands.router,
    open_profile.router,
    back_to_main.router,
    open_daily_tasks.router,
    add_daily_task.router,
    remove_daily_task.router,
    set_done_daily.router,
    daily_ok.router,
    daily_statistic.router,
]
