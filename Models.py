from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, UUID, DateTime

class Base(DeclarativeBase): pass

class Message(Base):
    __tablename__ = "messages"

    id: UUID = Column(UUID, primary_key=True, default=uuid4, index=True)
    user_id: UUID = Column(UUID, default=uuid4, index=True)
    text: str = Column(String)
    timestamp: datetime = Column(DateTime, default=datetime.now(timezone.utc))

class UserModel(Base):
    __tablename__ = "users"

    id: UUID = Column(UUID, primary_key=True, default=uuid4, index=True)
    name: str = Column(String)
    surname: str = Column(String)
    age: int = Column(Integer)
    email: str = Column(String)
    phone_number: str = Column(String)