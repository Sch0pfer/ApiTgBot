from api_v1.users import CreateUser
from fastapi import Depends, APIRouter
from uuid import UUID
from api_v1.users import crud
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("")
async def read_users(db: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.read_users(db)


@router.get("/{user_id}")
async def read_user(
    user_id: UUID, db: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.read_user(user_id, db)


@router.post("/")
async def create_user(
    user: CreateUser, db: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.create_user(user, db)


@router.delete("/{user_id}")
async def delete_user(
    user_id: UUID, db: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.delete_user(user_id, db)


@router.delete("/")
async def delete_users(db: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.delete_users(db)
