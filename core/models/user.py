from .base import Base

from sqlalchemy.orm import Mapped


class User(Base):
    username: Mapped[str]
    hashed_password: Mapped[str]
    age: Mapped[int]
    email: Mapped[str]
    phone: Mapped[str]
