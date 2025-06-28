from asyncio import current_task

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import scoped_session


from core.config import settings


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(url=url, echo=echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def get_scoped_session(self):
        session = scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def scoped_session_dependency(self):
        session = await self.get_scoped_session()
        yield session
        session.close()


db_helper = DatabaseHelper(
    url=settings.get_db_url(),
    echo=settings.DB_ECHO,
)
