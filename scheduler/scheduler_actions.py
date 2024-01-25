import json
from datetime import datetime

from aiogram import Bot
from aiogram_dialog import DialogManager
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.utils import send_reminder
from db.db_actions import get_tasks_from_db


async def add_job_to_scheduler(
        apscheduler: AsyncIOScheduler,
        manager: DialogManager,
        result: dict,
):
    apscheduler.add_job(
        send_reminder,
        **result["args"],
        kwargs={
            'bot': manager.event.bot, 'chat_id': manager.event.message.chat.id,
            'text': f'⚠️ {result["msg"]}'
        }
    )

# восстановление заданий из базы данных
async def recovery_job_to_scheduler(apscheduler: AsyncIOScheduler, bot: Bot):

    if tasks := await get_tasks_from_db():
        for task in tasks:
            tmp = json.loads(task.task_params)
            if rd := tmp["run_date"]:
                tmp["run_date"] = datetime.fromisoformat(rd)

            apscheduler.add_job(
                send_reminder,
                **tmp,
                kwargs={
                    'bot': bot, 'chat_id': task.chat_id,
                    'text': f'⚠️ {task.text}'
                }
            )