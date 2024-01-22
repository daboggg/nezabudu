from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import SwitchTo, Button, Row, Next, Cancel, Start, Back
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.help_dialog import HelpSG

main_dialog_router = Router()


class MainSG(StatesGroup):
    start = State()
    condition = State()
    text = State()
    total = State()


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
        "condition": dialog_manager.find("condition").get_value(),
        "text": dialog_manager.find("text").get_value()
    }


async def cancel_clicked(callback: CallbackQuery, button: Button, manager: DialogManager):
    await callback.message.answer("выберите команду в меню")


async def accept_clicked(callback: CallbackQuery, button: Button, manager: DialogManager):
    await callback.message.answer("добавлено")
    await manager.done()


main_dialog = Dialog(
    Window(
        Const("Если вы не знаете как пользоваться воспользуйтесь помощью в меню"),
        Const("= = = = = = = = = ="),
        Row(
            Start(Const("help"), id="help", state=HelpSG.start),
            Next(Const("далее"))
        ),
        state=MainSG.start
    ),
    Window(
        Const("Введите когда вы хотите получить напоминание(я)"),
        Const("= = = = = = = = = ="),
        TextInput(id="condition", on_success=next_state_or_finish_state),
        Row(
            Back(Const("назад")),
            Start(Const("help"), id="help", state=HelpSG.start),
        ),
        CANCEL_EDIT,
        state=MainSG.condition
    ),
    Window(
        Const("Введите текст напоминания"),
        Const("= = = = = = = = = ="),
        TextInput(id="text", on_success=next_state_or_finish_state),
        Row(
            Back(Const("назад")),
            Start(Const("help"), id="help", state=HelpSG.start),
        ),
        CANCEL_EDIT,
        state=MainSG.text
    )
    ,
    Window(
        Format("Напоминание будет: {condition}"),
        Format("С текстом: {text}"),
        Const("= = = = = = = = = ="),
        SwitchTo(Const("Изменить условие"), state=MainSG.condition, id="to_condition"),
        SwitchTo(Const("Изменить текст"), state=MainSG.text, id="to_text"),
        Start(Const("help"), id="help", state=HelpSG.start),
        Row(
            Cancel(Const("отмена"), on_click=cancel_clicked),
            Button(Const("принять"), id="accept", on_click=accept_clicked),
        ),
        state=MainSG.total,
        getter=result_getter
    ),
)


@main_dialog_router.message(CommandStart())
async def cmd_start(_, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(MainSG.start, mode=StartMode.RESET_STACK)
