from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper


async def get_async_session() -> AsyncSession:
    async with db_helper.session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
