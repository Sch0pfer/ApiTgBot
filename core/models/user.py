from .base import Base

from sqlalchemy.orm import Mapped


class User(Base):
    name: Mapped[str]
    surname: Mapped[str]
    age: Mapped[int]
    email: Mapped[str]
    phone: Mapped[str]
