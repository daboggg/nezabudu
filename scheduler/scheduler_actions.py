import json
from datetime import datetime

from aiogram import Bot
from aiogram_dialog import DialogManager
from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.utils import send_reminder
from db.db_actions import get_tasks_from_db


# добавление задание в скедулер
async def add_job_to_scheduler(
        apscheduler: AsyncIOScheduler,
        manager: DialogManager,
        result: dict,
        task_id: int,
)-> Job:
    job = apscheduler.add_job(
        send_reminder,
        **result["args"],
        id=str(task_id),
        name=str(manager.event.from_user.id),
        kwargs={
            'bot': manager.event.bot, 'chat_id': manager.event.from_user.id,
            'text': f'⚠️ {result["msg"]}'
        }
    )
    return job


# восстановление заданий из базы данных
async def recovery_job_to_scheduler(apscheduler: AsyncIOScheduler, bot: Bot):
    if tasks := await get_tasks_from_db():
        for task in tasks:
            tmp = json.loads(task.task_params)

            apscheduler.add_job(
                send_reminder,
                **tmp,
                id=str(task.id),
                name=str(task.chat_id),
                kwargs={
                    'bot': bot, 'chat_id': task.chat_id,
                    'text': f'⚠️ {task.text}'
                }
            )
