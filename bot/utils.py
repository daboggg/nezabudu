from aiogram import Bot
from aiogram.utils.formatting import as_list


# функция для отправки напомнаний
async def send_reminder(bot: Bot, chat_id: int, text: str, criterion: str) -> None:
    # фоматирование текста для напоминания
    format_text = as_list(
        "\t── ⋆⋅☆⋅⋆ ── ⋆⋅☆⋅⋆ ──",
        f"👉{text}👈",
        "\t── ⋆⋅☆⋅⋆ ── ⋆⋅☆⋅⋆ ──",
    )
    await bot.send_message(chat_id, format_text.as_html(), parse_mode='HTML')
