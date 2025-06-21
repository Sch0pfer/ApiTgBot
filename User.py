from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class User(BaseModel):
    id: UUID = Field(default_factory=uuid4, description="User ID")
    name: str
    surname: str
    age: int
    email: str
    phone_number: str