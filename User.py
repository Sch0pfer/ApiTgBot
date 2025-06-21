from pydantic import BaseModel

class User(BaseModel):
    name: str
    surname: str
    age: int
    email: str
    phone_number: str