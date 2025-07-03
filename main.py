from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.models import Base, db_helper
from api_v1.users import user_router
from core.logging_config import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


setup_logging()

app = FastAPI(lifespan=lifespan)
app.include_router(user_router)


@app.get("/")
async def root():
    return {"message": "Hello World!"}
