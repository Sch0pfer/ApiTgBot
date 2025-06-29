from api_v1.users import CreateUser, UserUpdate
from fastapi import Depends, APIRouter
from api_v1.users import crud
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from api_v1.users.dependencies import user_by_id
from core.models import db_helper, User

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/")
async def create_user(
    user: CreateUser, db: AsyncSession = Depends(db_helper.get_async_session)
):
    return await crud.create_user(user, db)


@router.get("/{user_id}")
async def read_user(
    user_id: UUID,
    db: AsyncSession = Depends(db_helper.get_async_session),
):
    return await crud.read_user(user_id, db)


@router.get("")
async def read_users(db: AsyncSession = Depends(db_helper.get_async_session)):
    return await crud.read_users(db)


@router.put("/{user_id}")
async def update_user(
    user_update: UserUpdate,
    user: User = Depends(user_by_id),
    db: AsyncSession = Depends(db_helper.get_async_session),
):
    return await crud.update_user(
        user_update=user_update,
        user=user,
        db=db,
    )


@router.delete("/{user_id}")
async def delete_user(
    user: User = Depends(user_by_id),
    db: AsyncSession = Depends(db_helper.get_async_session),
):
    return await crud.delete_user(user, db)


@router.delete("/")
async def delete_users(db: AsyncSession = Depends(db_helper.get_async_session)):
    return await crud.delete_users(db)
