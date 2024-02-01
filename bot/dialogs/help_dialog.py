from aiogram.utils.formatting import Bold, as_marked_section, as_list
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const

from bot.dialogs.state_groups import HelpSG

title = Bold("📌 Используйте примеры для установки напоминания.\n")
examples = as_marked_section(
    Bold("Например:"),
    "через 20 минут",
    "через 1 месяц, 2 дня, 6 часов",
    "через 1 год 20 минут",
    "в среду в 18.00",
    "в 13:30",
    "завтра в 23-36",
    "послезавтра в 23-36",
    "31 декабря в 22.17",
    "12.12.24 в 8.55",
    "каждый день 19-30",
    "каждую субботу в 13:14",
    "каждое 17 апреля",
    "каждое 14 число",
    "каждое 14 число в 12:12",
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
