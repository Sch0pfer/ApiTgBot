from uuid import UUID
from fastapi import FastAPI, HTTPException
from User import User
app = FastAPI()
users: list[User] = []

@app.get("/")
async def root():
    return {"message": "Hello World!"}
@app.get("/users")
async def read_users():
    return {"users": users}

@app.get("/users/{user_id}")
async def read_user(user_id: UUID):
    for user in users:
        if user.id == user_id:
            return {"user_id": user_id,
                    "name": user.name,
                    "surname": user.surname,
                    "age": user.age,
                    "email": user.email,
                    "phone_number": user.phone_number}
    return HTTPException(status_code=404, detail="User not found")

@app.post("/users/")
async def create_user(user: User):
    users.append(user)
    return {"message": f"User {user.name} created successfully!"}