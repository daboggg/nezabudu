from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, relationship

from models import Base


class Task(Base):

    task_params: Mapped[str]
    chat_id: Mapped[int]
    text: Mapped[str]
    criterion: Mapped[str]
