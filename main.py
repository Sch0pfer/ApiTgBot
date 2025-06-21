from fastapi import FastAPI
from User import User
app = FastAPI()
WhiteGuy = User(name="Mathew",surname="Balls",age=18,email="<EMAIL>",phone_number="+5555555555")
users: list[User] = [WhiteGuy]

@app.get("/users")
async def read_users():
    return {"users": users}

@app.get("/users/{user_id}")
async def read_user(user_id: int):
    return {"user_id": user_id,
            "name": users[user_id].name,
            "surname": users[user_id].surname,
            "age": users[user_id].age,
            "email": users[user_id].email,
            "phone_number": users[user_id].phone_number}

@app.post("/users/")
async def create_user(user: User):
    if not any(existing_user.name == user.name for existing_user in users):
        users.append(user)
        return {"message": f"User {user.name} created successfully!"}
    else:
        return {"error": "User already exists!"}