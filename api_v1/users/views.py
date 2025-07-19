from typing import Optional
from pydantic import EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from api_v1.users import CreateUser, UserUpdate
from fastapi import Depends, APIRouter, Query, HTTPException, status
from api_v1.users import crud
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from api_v1.users.dependencies import get_current_user, user_by_id
from core.models import db_helper, User

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.post(
    path="/",
    status_code=201,
)
async def create_user(user: CreateUser, db: AsyncSession = Depends(db_helper.get_db)):
    return await crud.create_user(user, db)


@router.get(path="/me", status_code=200)
async def read_current_user(
    user: User = Depends(get_current_user),
):
    return user


@router.get(path="/{user_id}", status_code=200)
async def read_user(
    user_id: UUID,
    db: AsyncSession = Depends(db_helper.get_db),
):
    return await crud.read_user(user_id, db)


@router.get(
    path="",
    status_code=200,
)
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


@router.put(
    path="/{user_id}",
    status_code=204,
)
async def update_user(
    user_update: UserUpdate,
    target_user: User = Depends(user_by_id),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(db_helper.get_db),
):
    if current_user.id != target_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user",
        )
    return await crud.update_user(
        user_update=user_update,
        user=target_user,
        db=db,
    )


@router.delete(
    path="/{user_id}",
    status_code=204,
)
async def delete_user(
    target_user: User = Depends(user_by_id),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(db_helper.get_db),
):
    if current_user.id != target_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user",
        )
    return await crud.delete_user(target_user, db)


@router.delete(
    path="/",
    status_code=204,
)
async def delete_users(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(db_helper.get_db),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can delete all users",
        )
    return await crud.delete_users(db)
