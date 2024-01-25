import json

from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_helper import db_helper
from models import Task



async def add_task_to_db(manager, result, session: AsyncSession):
    # если run_date присутствует в словаре, преобразуем datetime в строку
    if rd := result.get("args").get("run_date"):
        result["args"]["run_date"] = str(rd)

    task = Task(
        task_params=json.dumps(result["args"]),
        chat_id=manager.event.message.chat.id,
        text=manager.find('text').get_value()
    )
    session.add(task)
    await session.commit()
    await session.close()

async def get_tasks_from_db()->list[Task]:
    session = db_helper.get_scoped_session()

    result: Result = await session.execute(select(Task))
    await session.close()
    tasks = result.scalars().all()

    return list(tasks)