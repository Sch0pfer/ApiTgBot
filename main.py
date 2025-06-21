from uuid import UUID
from fastapi import FastAPI, HTTPException
from Models import UserModel, Message, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from User import User

SQLALCHEMY_DATABASE_URL = "sqlite:///sql_app.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(autoflush=False, bind=engine)
db = Session()
app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Hello World!"}
@app.get("/users")
async def read_users():
    return {"users": db.query(UserModel).all()}

@app.get("/users/{user_id}")
async def read_user(user_id: UUID):
    current_user = db.get(UserModel, user_id)
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    return current_user

@app.post("/users/")
async def create_user(user: User):
    db_user = UserModel(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": f"User {user.name} created successfully!"}