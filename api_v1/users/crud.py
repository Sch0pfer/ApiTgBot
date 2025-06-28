from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from core.models import User
from fastapi import HTTPException
from api_v1.users.schemas import CreateUser
from uuid import UUID


async def read_users(db: AsyncSession):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return {"users": users}


async def read_user(user_id: UUID, db: AsyncSession):
    current_user = await db.get(User, user_id)
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": current_user}


async def create_user(user: CreateUser, db: AsyncSession):
    db_user = User(**user.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return {"message": f"User {user.name} created successfully!"}


async def delete_user(user_id: UUID, db: AsyncSession):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(user)
    await db.commit()
    await db.refresh(user)
    return {"message": f"User {user.name} deleted successfully!"}


async def delete_users(db: AsyncSession):
    await db.execute(delete(User))
    await db.commit()
    await db.refresh(User)
    return {"message": "Users deleted successfully!"}
