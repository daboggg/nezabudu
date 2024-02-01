from aiogram.fsm.state import StatesGroup, State


class HelpSG(StatesGroup):
    start = State()


class ListOfRemindersSG(StatesGroup):
    start = State()
    remind = State()


class MainSG(StatesGroup):
    criterion = State()
    text = State()
    total = State()
    select = State()
