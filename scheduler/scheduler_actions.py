from aiogram_dialog import DialogManager
from apscheduler.schedulers.asyncio import AsyncIOScheduler


async def add_job_to_scheduler(
        apscheduler: AsyncIOScheduler,
        manager: DialogManager,
        result: dict,
        send_reminder
):
    apscheduler.add_job(
        send_reminder,
        **result["args"],
        kwargs={
            'bot': manager.event.bot, 'chat_id': manager.event.message.chat.id,
            'text': f'⚠️ {result["msg"]}'
        }
    )
