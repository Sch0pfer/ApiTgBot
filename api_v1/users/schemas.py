from pydantic import BaseModel, Field, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from uuid import UUID, uuid4


class CreateUser(BaseModel):
    id: UUID = Field(default_factory=uuid4, description="UUID of the user")
    name: str
    surname: str
    age: int
    email: EmailStr
    phone: PhoneNumber


class UpdateUser(CreateUser):
    pass


class UpdateUserPartial(BaseModel):
    name: str | None
    surname: str | None
    age: int | None
    email: EmailStr | None
    phone: PhoneNumber | None
