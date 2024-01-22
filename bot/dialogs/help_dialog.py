from aiogram.fsm.state import StatesGroup, State
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const


class HelpSG(StatesGroup):
    start = State()


help_dialog = Dialog(
    Window(
        Const("помощь помощь помощь"),
        Cancel(Const("назад")),
        state=HelpSG.start
    ),

)
