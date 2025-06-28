from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from uuid import UUID
from fastapi import Path, Depends, status, HTTPException

from core.models import db_helper, User
from . import crud


async def user_by_id(
    user_id: Annotated[UUID, Path],
    db: AsyncSession = Depends(db_helper.get_async_session),
) -> User:
    user = await crud.read_user(user_id, db)
    if user:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found",
    )
