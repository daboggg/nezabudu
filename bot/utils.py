from aiogram import Bot

# функция для отправки напомнаний
async def send_reminder(bot: Bot, chat_id: int, text: str) -> None:
    await bot.send_message(chat_id, text, parse_mode='HTML')
