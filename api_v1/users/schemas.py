from pydantic import BaseModel, Field, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from uuid import UUID, uuid4


class UserBase(BaseModel):
    name: str
    surname: str
    age: int
    email: EmailStr
    phone: PhoneNumber


class CreateUser(UserBase):
    id: UUID = Field(default_factory=uuid4, description="UUID of the user")


class UserUpdate(UserBase):
    pass


class UserUpdatePartial(UserBase):
    name: str | None = None
    surname: str | None = None
    age: int | None = None
    email: EmailStr | None = None
    phone: PhoneNumber | None = None