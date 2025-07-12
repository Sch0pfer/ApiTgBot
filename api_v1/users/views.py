from typing import Optional

from pydantic import EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

from api_v1.users import CreateUser, UserUpdate
from fastapi import Depends, APIRouter, Query
from api_v1.users import crud
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from api_v1.users.dependencies import user_by_id
from core.models import db_helper, User

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.post("/", status_code=201)
async def create_user(user: CreateUser, db: AsyncSession = Depends(db_helper.get_db)):
    return await crud.create_user(user, db)


@router.get("/{user_id}")
async def read_user(
    user_id: UUID,
    db: AsyncSession = Depends(db_helper.get_db),
):
    return await crud.read_user(user_id, db)


@router.get("")
async def read_users(
    db: AsyncSession = Depends(db_helper.get_db),
    username: Optional[str] = None,
    age: Optional[int] = None,
    email: Optional[EmailStr] = None,
    phone: Optional[PhoneNumber] = None,
    min_id: Optional[int] = None,
    max_id: Optional[int] = None,
    skip: Optional[int] = None,
    limit: Optional[int] = None,
    sort: Optional[str] = Query(
        None, description="Sort field (id, username, age, email, phone"
    ),
    order: Optional[str] = Query("asc", description="Sort direction (asc or desc)"),
):
    return await crud.read_users(
        db,
        username=username,
        age=age,
        email=email,
        phone=phone,
        min_id=min_id,
        max_id=max_id,
        skip=skip,
        limit=limit,
        sort=sort,
        order=order,
    )


@router.put("/{user_id}")
async def update_user(
    user_update: UserUpdate,
    user: User = Depends(user_by_id),
    db: AsyncSession = Depends(db_helper.get_db),
):
    return await crud.update_user(
        user_update=user_update,
        user=user,
        db=db,
    )


@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user: User = Depends(user_by_id),
    db: AsyncSession = Depends(db_helper.get_db),
):
    return await crud.delete_user(user, db)


@router.delete("/", status_code=204)
async def delete_users(db: AsyncSession = Depends(db_helper.get_db)):
    return await crud.delete_users(db)
