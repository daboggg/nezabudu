import json

from models import Task


async def add_task_to_db(manager, result, session):
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
