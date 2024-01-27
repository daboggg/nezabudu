from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.formatting import Bold, as_marked_section, as_list
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const


class HelpSG(StatesGroup):
    start = State()

title = Bold("📌 Используйте примеры для установки напоминания.\n")
examples = as_marked_section(
    Bold("Например:"),
    "через 20 минут",
    "через 1 месяц, 2 дня, 6 часов",
    "через 20 минут",
    "в среду в 18.00",
    "в 13:30",
    "завтра в 23-36",
    "31 декабря в 22.17",
    "12.12.24 в 8.55",
    "каждый день 19-30",
    "каждую субботу в 13:14",
    "каждое 17 апреля",
    marker="✔️ "
    )
help_text = as_list(title, examples)


help_dialog = Dialog(
    Window(
        Const(help_text.as_html()),
        Cancel(Const("назад")),
        state=HelpSG.start
    ),

)
