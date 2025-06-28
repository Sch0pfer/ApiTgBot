from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.models import Base, db_helper
from api_v1.users import user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    try:
        yield
    finally:
        await db_helper.engine.close_connection()


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)


@app.get("/")
async def root():
    return {"message": "Hello World!"}
