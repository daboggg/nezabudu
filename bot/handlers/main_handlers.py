from datetime import datetime, timedelta

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from parser.core import remind_formatter

main_handlers_router = Router()


async def send_reminder(bot: Bot, chat_id: int, text: str) -> None:
    await bot.send_message(chat_id, text, parse_mode='HTML')


@main_handlers_router.message(Command(commands=['start']))
async def cmd_start(message: Message):
    reply_text1 = '🚂 Привет, это бот для определения даты покупки билетов за 45, 60 или 90 дней.'

    await message.answer(text=reply_text1)


@main_handlers_router.message(F.text == "bbb")
async def get_remind(message: Message, bot: Bot, apscheduler: AsyncIOScheduler):
    print(apscheduler.get_jobs())
    await message.answer("aaa")


@main_handlers_router.message(F.text == "aaa")
async def get_remind(message: Message, bot: Bot, apscheduler: AsyncIOScheduler):
    # prm = start("через 1 минуты@ как дела ")
    prm = remind_formatter("каждую пятницу в 15:23@ как делишки?")
    print(prm.get("args"))
    apscheduler.add_job(send_reminder,
                        # id=id,
                        # run_date=datetime.now() + timedelta(minutes=1),
                        # run_date=datetime(
                        #     dop.year,
                        #     dop.month,
                        #     dop.day,
                        #     7,
                        #     50,
                        #     0
                        # ),
                        kwargs={'bot': bot, 'chat_id': message.from_user.id,
                                'text': f'⚠️ {prm.get("msg")}'},
                        **prm.get('args')
                        )

    await message.answer(f'✔️Вы получите напоминание')

