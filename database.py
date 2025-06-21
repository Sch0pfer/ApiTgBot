from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy import  Column, Integer, String, UUID, DateTime

SQLALCHEMY_DATABASE_URL = "sqlite:///sql_app.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

Session = sessionmaker(autoflush=False, bind=engine)

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