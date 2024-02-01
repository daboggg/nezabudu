from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='добавить напоминание'
        ),
        # BotCommand(
        #     command='help',
        #     description='помощь'
        # ),
        BotCommand(
            command='list_of_reminds',
            description='список напоминаний'
        ),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())