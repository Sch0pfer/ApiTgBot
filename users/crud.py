from fastapi import HTTPException

from users.schemas import User

from database import *

from uuid import UUID

Base.metadata.create_all(bind=engine)

def read_users(db: Session):
    users = db.query(UserModel).all()
    return {"users": users}

def read_user(user_id: UUID, db: Session):
    current_user = db.get(UserModel, user_id)
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": current_user}

def create_user(user: User, db: Session):
    db_user = UserModel(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": f"User {user.name} created successfully!"}

def delete_user(user_id: UUID, db: Session):
    user = db.get(UserModel, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": f"User {user.name} deleted successfully!"}

def delete_users(db: Session):
    db_users = db.query(UserModel).all()
    if not db_users:
        raise HTTPException(status_code=404, detail="User not found")
    for db_user in db_users:
        db.delete(db_user)
    db.commit()
    return {"message": "Users deleted successfully!"}