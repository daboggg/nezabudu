from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.utils.formatting import as_list, Bold, Italic, as_marked_section, as_key_value
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import SwitchTo, Button, Row, Cancel, Start, Back
from aiogram_dialog.widgets.text import Const, Format
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import AsyncSession

from bot.dialogs.state_groups import HelpSG, ListOfRemindersSG, MainSG
from db.db_actions import add_task_to_db
from parser.core import remind_formatter
from scheduler.scheduler_actions import add_job_to_scheduler

CANCEL_EDIT = SwitchTo(
    Const("Отменить редактирование"),
    when=F["dialog_data"]["finished"],
    id="cnl_edt",
    state=MainSG.total,
)


async def next_state_or_finish_state(event, widget, dialog_manager: DialogManager, *_):
    if dialog_manager.dialog_data.get("finished"):
        await dialog_manager.switch_to(MainSG.total)
    else:
        await dialog_manager.next()


async def result_getter(dialog_manager: DialogManager, **kwargs):
    dialog_manager.dialog_data["finished"] = True
    return {
        "criterion": dialog_manager.find("criterion").get_value(),
        "text": dialog_manager.find("text").get_value()
    }


async def cancel_clicked(callback: CallbackQuery, button: Button, manager: DialogManager):
    manager.dialog_data["finished"] = False


async def accept_clicked(callback: CallbackQuery, button: Button, manager: DialogManager):
    session: AsyncSession = manager.middleware_data.get("session")
    apscheduler: AsyncIOScheduler = manager.middleware_data.get("apscheduler")

    task = f"{manager.find('criterion').get_value()} @ {manager.find('text').get_value()}"

    try:
        result = remind_formatter(task)

        task_id = await add_task_to_db(manager, result, session)
        await add_job_to_scheduler(apscheduler, manager, result, task_id)

        await manager.next()
    except Exception as e:
        await callback.message.answer(str(e))
        await callback.message.answer("💡 для продолжения воспользуйтесь меню")
        await manager.done()


async def add_task_clicked(callback: CallbackQuery,
                           button: Button,
                           dialog_manager: DialogManager):
    dialog_manager.dialog_data["finished"] = False


async def list_tasks_clicked(cq: CallbackQuery,
                             button: Button,
                             dialog_manager: DialogManager):
    await dialog_manager.done()


# форматированный текст для главного диалога
separator = "✦ ✦ ✦ ✦ ✦ ✦ ✦ ✦ ✦"
start_text = as_list(
    Bold("💡 Если вы не знаете как пользоваться воспользуйтесь помощью👇"),
    separator
)
criterion_text = as_list(
    Bold("💡 Когда вы хотите получить напоминание❓"),
    Italic("введите текст ..🖋"),
    separator
)
task_text = as_list(
    Bold("💡 Введите текст напоминания"),
    separator
)
total_text = Format(
    as_list(
        as_marked_section(
            Bold("💡 Проверьте!:"),
            as_key_value("Напоминание придет", Italic("{criterion}")),
            as_key_value("С текстом", Italic("{text}")),
            marker="✔️ "
        ),
        separator,
    ).as_html()),

# главный диалог
main_dialog = Dialog(
    Window(
        Const(criterion_text.as_html()),
        TextInput(id="criterion", on_success=next_state_or_finish_state),
        Row(
            Start(Const("список напоминаний"), id="list_tasks", state=ListOfRemindersSG.start,
                  on_click=list_tasks_clicked),
            Start(Const("помощь"), id="help", state=HelpSG.start),
        ),
        CANCEL_EDIT,
        state=MainSG.criterion
    ),
    Window(
        Const(task_text.as_html()),
        TextInput(id="text", on_success=next_state_or_finish_state),
        Row(
            Back(Const("назад")),
            Start(Const("помощь"), id="help", state=HelpSG.start),
        ),
        CANCEL_EDIT,
        state=MainSG.text
    )
    ,
    Window(
        *total_text,
        SwitchTo(Const("изменить условие"), state=MainSG.criterion, id="to_criterion"),
        SwitchTo(Const("изменить текст"), state=MainSG.text, id="to_text"),
        Start(Const("помощь"), id="help", state=HelpSG.start),
        Row(
            SwitchTo(Const("отмена"), on_click=cancel_clicked, id='cancel', state=MainSG.criterion),
            Button(Const("принять"), id="accept", on_click=accept_clicked),
        ),
        state=MainSG.total,
        getter=result_getter
    ),
    Window(
        Const(f"💡 Напоминание добавлено!"),
        Row(
            SwitchTo(Const("добавить напоминание"), state=MainSG.criterion, id="add_task", on_click=add_task_clicked),
            Start(Const("список напоминаний"), id="list_tasks", state=ListOfRemindersSG.start,
                  on_click=list_tasks_clicked),
        ),
        state=MainSG.select
    ),
)
