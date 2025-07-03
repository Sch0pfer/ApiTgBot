from typing import Optional

from pydantic import EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from uuid import UUID

from core.models import User
from fastapi import HTTPException
from api_v1.users import CreateUser, UserUpdate, UserUpdatePartial


async def create_user(user: CreateUser, db: AsyncSession):
    db_user = User(**user.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return {"message": f"User {user.name} created successfully!"}


async def read_user(user_id: UUID, db: AsyncSession):
    return await db.get(User, user_id)


async def read_users(
    db: AsyncSession,
    name: Optional[str] = None,
    surname: Optional[str] = None,
    age: Optional[int] = None,
    email: Optional[EmailStr] = None,
    phone: Optional[PhoneNumber] = None,
    min_id: Optional[int] = None,
    max_id: Optional[int] = None,
    skip: Optional[int] = None,
    limit: Optional[int] = None,
    sort: Optional[str] = None,
    order: Optional[str] = "asc",
):
    allowed_sort_fields = ["id", "name", "surname", "age", "email", "phone"]
    order_direction = order.strip().lower() if order else "asc"

    filters = []
    if name is not None:
        filters.append(User.name.ilike(f"%{name}%"))
    if surname is not None:
        filters.append(User.surname.ilike(f"%{surname}%"))
    if age is not None:
        filters.append(User.age == age)
    if email is not None:
        filters.append(User.email == email)
    if phone is not None:
        filters.append(User.phone == phone)
    if min_id is not None:
        filters.append(User.id >= min_id)
    if max_id is not None:
        filters.append(User.id <= max_id)

    query = select(User)
    if filters:
        query = query.filter(*filters)

    if sort and sort in allowed_sort_fields:
        sort_field = getattr(User, sort)
        if order_direction == "desc":
            query = query.order_by(sort_field.desc())
        else:
            query = query.order_by(sort_field.asc())
    else:
        query = query.order_by(sort_field.asc())

    if skip is not None:
        query = query.offset(skip)
    if limit is not None:
        query = query.limit(limit)

    result = await db.execute(query)
    users = result.scalars().all()
    return {"users": users}


async def update_user(
    db: AsyncSession,
    user: User,
    user_update: UserUpdate | UserUpdatePartial,
    partial: bool = False,
) -> User:
    for name, value in user_update.model_dump(exclude_unset=partial).items():
        setattr(user, name, value)
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(user: User, db: AsyncSession):
    user = await db.get(User, user.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(user)
    await db.commit()
    return {"message": f"User {user.name} deleted successfully!"}


async def delete_users(db: AsyncSession):
    await db.execute(delete(User))
    await db.commit()
    return {"message": "Users deleted successfully!"}
