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

    async def get_async_session(self):
        async with self.session_factory() as session:
            try:
                yield session
            finally:
                await session.close()

db_helper = DatabaseHelper(
    url=settings.get_db_url(),
    echo=settings.DB_ECHO,
)
