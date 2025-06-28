from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from uuid import UUID

from core.models import User
from fastapi import HTTPException
from api_v1.users import CreateUser, UpdateUser, UpdateUserPartial


async def create_user(user: CreateUser, db: AsyncSession):
    db_user = User(**user.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return {"message": f"User {user.name} created successfully!"}


async def read_user(user_id: UUID, db: AsyncSession):
    return await db.get(User, user_id)


async def read_users(db: AsyncSession):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return {"users": users}


async def update_user(
    user: User,
    db: AsyncSession,
    user_update: UpdateUser | UpdateUserPartial,
    partial: bool = False,
) -> User:
    for name, value in user_update.model_dump(exclude_unset=partial).items():
        setattr(user, name, value)
    await db.commit()
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
