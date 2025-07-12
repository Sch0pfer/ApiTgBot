from contextlib import asynccontextmanager

from authx.exceptions import MissingTokenError
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from api_v1.users import user_router
from api_v1.users import auth_router
from core.logging_config import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


setup_logging()

app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(auth_router)


@app.exception_handler(MissingTokenError)
async def handle_missing_token(request: Request, exc: MissingTokenError):
    return JSONResponse(
        status_code=401,
        content={"detail": "Missing access token"},
    )
