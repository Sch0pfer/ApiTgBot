import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from uuid import UUID
from fastapi import Path, Depends, status, HTTPException, Request, Depends
from authx import AuthX

from core.models import db_helper, User
from core.config import settings
from . import crud


async def user_by_id(
    user_id: Annotated[UUID, Path],
    db: AsyncSession = Depends(db_helper.get_db),
) -> User:
    user = await crud.read_user(user_id, db)
    if user:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found",
    )


async def get_current_user_id(
    request: Request,
) -> UUID:
    token = request.cookies.get(settings.JWT_ACCESS_COOKIE_NAME)

    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        user_data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return UUID(user_data["sub"])
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=401, detail="Invalid token") from e


async def get_current_user(
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(db_helper.get_db),
) -> User:
    user = await crud.read_user(user_id, db)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found",
    )
