from datetime import datetime, timezone

from uuid import uuid4

from pydantic_extra_types.phone_numbers import PhoneNumber

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy import  Column, Integer, String, UUID, DateTime

from pydantic import EmailStr

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


SQLALCHEMY_DATABASE_URL = "sqlite:///sql_app.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

Session = sessionmaker(autoflush=False, bind=engine)

class Base(DeclarativeBase): pass

class UserModel(Base):
    __tablename__ = "users"

    id: UUID = Column(UUID, primary_key=True, default=uuid4, index=True)
    name: str = Column(String)
    surname: str = Column(String)
    age: int = Column(Integer)
    email: EmailStr = Column(String)
    phone_number: PhoneNumber = Column(String)