import json
import logging

import apscheduler.events
from aiogram_dialog import DialogManager
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_helper import db_helper, sync_db_helper
from models import Task


logger = logging.getLogger(__name__)


# добавить задание в бд
async def add_task_to_db(manager: DialogManager, result: dict, session: AsyncSession) -> int:

    # если run_date присутствует в словаре, преобразуем datetime в строку
    if rd := result.get("args").get("run_date"):
        result["args"]["run_date"] = str(rd)

    task = Task(
        task_params=json.dumps(result["args"]),
        chat_id=manager.event.from_user.id,
        text=manager.find('text').get_value(),
        criterion=manager.find('criterion').get_value()
    )
    session.add(task)
    await session.flush()
    task_id = task.id
    await session.commit()
    await session.close()

    return task_id


# взять все задания из бд
async def get_tasks_from_db() -> list[Task]:
    session = db_helper.get_scoped_session()

    result: Result = await session.execute(select(Task))
    tasks = result.scalars().all()
    await session.close()

    return list(tasks)


# удалить задание из бд
def sync_delete_task_from_db(job: apscheduler.events.JobEvent):
    session = sync_db_helper.session_factory()
    task = session.get(Task, job.job_id)
    logger.info(f"удален job с id: {job.job_id}" )
    session.delete(task)
    session.commit()
    session.close()
