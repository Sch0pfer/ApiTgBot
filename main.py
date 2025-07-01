from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.models import Base, db_helper
from api_v1.users import user_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    yield

app = FastAPI(lifespan=lifespan)
app.include_router(user_router)


@app.get("/")
async def root():
    return {"message": "Hello World!"}
