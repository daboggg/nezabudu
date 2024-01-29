from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from bot.dialogs.list_of_remiders_dialog import ListOfRemindersSG
from bot.dialogs.main_dialog import MainSG

cmd_router = Router()


@cmd_router.message(CommandStart())
async def cmd_start(_, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(MainSG.start, mode=StartMode.RESET_STACK)


@cmd_router.message(Command(commands="help"))
async def cmd_start(message: Message) -> None:
    await message.answer("помощь помощь")


@cmd_router.message(Command(commands="list_of_reminds"))
async def cmd_start(_, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(ListOfRemindersSG.start, mode=StartMode.RESET_STACK)
