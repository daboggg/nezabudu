import operator
from typing import Any

from aiogram.types import CallbackQuery
from aiogram.utils.formatting import Bold, as_key_value, as_marked_section
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Select, Column, Back, Button, Row, Start
from aiogram_dialog.widgets.text import Const, Format, Case
from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.dialogs.state_groups import ListOfRemindersSG, MainSG


async def window1_get_data(**kwargs):
    manager: DialogManager = kwargs["dialog_manager"]
    user_id = manager.event.from_user.id
    list_of_reminds_tmp: list[Job] = kwargs["apscheduler"].get_jobs()
    # фильтрую список Job по user_id
    list_of_reminds = list(filter(lambda j: int(j.name) == user_id, list_of_reminds_tmp))
    is_not_empty = "True" if list_of_reminds else "False"
    print(is_not_empty)
    return {
        "reminds": [
            (f"{remind.kwargs['criterion']}   {remind.kwargs['text']}", remind.id)
            for remind in list_of_reminds
        ],
        "is_not_empty": is_not_empty
    }


async def window2_get_data(**kwargs):
    manager: DialogManager = kwargs["dialog_manager"]
    scheduler: AsyncIOScheduler = manager.middleware_data.get("apscheduler")
    remind_id = manager.dialog_data.get("s_reminds")
    job: Job = scheduler.get_job(remind_id)
    # тект напоминания
    remind_text = as_marked_section(
        Bold("‼️ НАПОМИНАНИЕ:"),
        as_key_value("придет", job.kwargs.get("criterion")),
        as_key_value("с текстом", job.kwargs.get("text")),
        as_key_value("следующий запуск", job.next_run_time.replace(tzinfo=None).replace(microsecond=0)),
        marker="✔️ "
    ).as_html()
    return {
        "remind_text": remind_text
    }


async def on_remind_selected(callback: CallbackQuery, widget: Any,
                             manager: DialogManager, item_id: str):
    manager.dialog_data["s_reminds"] = item_id
    await manager.next()


async def on_delete(callback: CallbackQuery, button: Button,
                    manager: DialogManager):
    scheduler: AsyncIOScheduler = manager.middleware_data.get("apscheduler")
    job_id: str = manager.dialog_data["s_reminds"]
    scheduler.remove_job(job_id)
    await callback.answer("Напоминание удалено")
    await manager.back()


async def new_task_clicked(cq: CallbackQuery,
                           button: Button,
                           dialog_manager: DialogManager):
    await dialog_manager.done()


list_of_reminders_dialog = Dialog(
    Window(
        # Const("📄 Список напоминаний"),
        Case(
            {
                "True": Const("📄 Список напоминаний: 👇"),
                "False": Const("📄 Список пустой 🫲   🫱"),
            },
            selector="is_not_empty"
        ),
        Column(
            Select(
                Format("{item[0]}"),
                id="s_reminds",
                items="reminds",
                item_id_getter=operator.itemgetter(1),
                on_click=on_remind_selected,
            ),
        ),
        Start(Const("добавить напоминание"), id="new_task", state=MainSG.criterion, on_click=new_task_clicked),
        state=ListOfRemindersSG.start,
        getter=window1_get_data,
    ),
    Window(
        Format("{remind_text}"),
        Row(
            Back(Const("назад")),
            Button(Const("удалить"), on_click=on_delete, id="delete_remind"),
        ),
        state=ListOfRemindersSG.remind,
        getter=window2_get_data,

    ),
)
