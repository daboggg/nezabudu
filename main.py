import asyncio
import logging

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.handlers.main_handlers import main_handlers_router
from bot.middlewares.apschedmiddleware import SchedulerMiddleware
from settings import settings
from utils.comands import set_commands


async def start_bot(bot):
    await set_commands(bot)
    # await bot.send_message(settings.bots.admin_id, text='Бот запущен')
    await bot.send_message(settings.bots.admin_id, text='Бот запущен')


async def stop_bot(bot):
    await bot.send_message(settings.bots.admin_id, text='Бот остановлен')


async def start():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - [%(levelname)s - %(name)s - '
                               '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'

                        )
    logger = logging.getLogger('main')

    # Создаю и запускаю шедулер
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.start()

    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')

    dp = Dispatcher()

    # регистрация middlewares
    dp.update.middleware.register(SchedulerMiddleware(scheduler))

    # подключение роутеров
    dp.include_routers(
        main_handlers_router
    )

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    logger.info('start')

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(start())