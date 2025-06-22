from fastapi import FastAPI, HTTPException, Depends
from database import *
from User import User
from uuid import UUID

Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Hello World!"}
@app.get("/users")
async def read_users(db: Session = Depends(get_db)):
    return {"users": db.query(UserModel).all()}

@app.get("/users/{user_id}")
async def read_user(user_id: UUID, db: Session = Depends(get_db)):
    current_user = db.get(UserModel, user_id)
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": current_user}

@app.post("/users/")
async def create_user(user: User, db: Session = Depends(get_db)):
    db_user = UserModel(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": f"User {user.name} created successfully!"}

@app.delete("/users/{user_id}")
async def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    user = db.get(UserModel, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": f"User {user.name} deleted successfully!"}

@app.delete("/users/")
async def delete_users(db: Session = Depends(get_db)):
    db_users = db.query(UserModel).all()
    if not db_users:
        raise HTTPException(status_code=404, detail="User not found")
    for db_user in db_users:
        db.delete(db_user)
    db.commit()
    return {"message": "Users deleted successfully!"}