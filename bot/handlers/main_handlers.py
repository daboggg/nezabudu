from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

main_handlers_router = Router()
@main_handlers_router.message(Command(commands=['start']))
async def cmd_start(message: Message):
    reply_text1 = '🚂 Привет, это бот для определения даты покупки билетов за 45, 60 или 90 дней.'

    await message.answer(text=reply_text1)