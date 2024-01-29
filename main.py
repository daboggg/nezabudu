import asyncio
import logging

import apscheduler.events
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.dialogs.list_of_remiders_dialog import list_of_reminders_dialog
from bot.dialogs.main_dialog import main_dialog
from bot.dialogs.help_dialog import help_dialog
from bot.handlers.cmd import cmd_router
from bot.middlewares.apschedmiddleware import SchedulerMiddleware
from db.db_actions import sync_delete_task_from_db
from db.db_helper import db_helper
from scheduler.scheduler_actions import recovery_job_to_scheduler
from settings import settings
from bot.comands import set_commands


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text='Бот запущен')

scheduler: AsyncIOScheduler

async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Бот остановлен')
    scheduler.shutdown()


async def start():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - [%(levelname)s - %(name)s - '
                               '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'

                        )
    logger = logging.getLogger('main')

    # Создаю и запускаю шедулер
    global scheduler
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")


    # слушатель на событие удаления job
    scheduler.add_listener(sync_delete_task_from_db, apscheduler.events.EVENT_JOB_REMOVED)
    scheduler.start()



    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')

    # восстановление заданий при старте из базы данных
    await recovery_job_to_scheduler(scheduler, bot)

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage, session=db_helper.get_scoped_session())

    # регистрация middlewares
    dp.update.middleware.register(SchedulerMiddleware(scheduler))


    # подключение роутеров
    dp.include_routers(
        cmd_router,
        main_dialog,
        help_dialog,
        list_of_reminders_dialog,
    )

    # подключение диалогов
    setup_dialogs(dp)

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    logger.info('start')

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(start())

