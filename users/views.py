from users.schemas import User

from fastapi import Depends, APIRouter

from database import *

from uuid import UUID

from users import crud

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("")
async def read_users(db: Session = Depends(get_db)):
    return crud.read_users(db)


@router.get("/{user_id}")
async def read_user(user_id: UUID, db: Session = Depends(get_db)):
    return crud.read_user(user_id, db)


@router.post("/")
async def create_user(user: User, db: Session = Depends(get_db)):
    return crud.create_user(user, db)


@router.delete("/{user_id}")
async def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    return crud.delete_user(user_id, db)


@router.delete("/")
def delete_users(db: Session = Depends(get_db)):
    return crud.delete_users(db)
