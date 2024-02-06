from asyncio import current_task

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session, AsyncSession
from sqlalchemy.orm import sessionmaker

from settings import settings


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=url,
            echo=echo
        )
        self.session_factory = async_sessionmaker(
            self.engine,
        )
    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task
        )
        return session

    async def session(self) -> AsyncSession:
        session = self.get_scoped_session()
        async with session() as sess:
            yield sess
            await session.remove()


db_helper = DatabaseHelper(url=settings.db.async_db_url,echo=settings.db.db_echo)
