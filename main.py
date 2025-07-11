from contextlib import asynccontextmanager
from fastapi import FastAPI
from api_v1.users import user_router
from core.logging_config import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


setup_logging()

app = FastAPI(lifespan=lifespan)
app.include_router(user_router)


@app.get("/api/v1/")
async def root():
    return {"message": "Hello World!"}
