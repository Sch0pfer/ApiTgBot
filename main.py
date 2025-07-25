import logging
from contextlib import asynccontextmanager
from typing import Callable
from authx.exceptions import MissingTokenError
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from api_v1.users import user_router
from api_v1.users import auth_router
from core.logging_config import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:8000",
    "http://localhost:3000",
]


@app.middleware("http")
async def middleware(request: Request, call_next: Callable) -> Response:
    logger.info(
        f"Request started",
        extra={
            "method": request.method,
            "url": str(request.url),
            "headers": dict(request.headers),
        },
    )

    try:
        response = await call_next(request)
    except Exception as e:
        logger.error(
            "Request failed",
            exc_info=e,
            extra={
                "method": request.method,
                "url": str(request.url),
            },
        )
        raise

    logger.info(
        f"Request completed",
        extra={
            "method": request.method,
            "url": str(request.url),
            "status_code": response.status_code,
            "response_headers": dict(response.headers),
        },
    )
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user_router)
app.include_router(auth_router)


@app.exception_handler(MissingTokenError)
async def handle_missing_token(request: Request, exc: MissingTokenError):
    return JSONResponse(
        status_code=401,
        content={"detail": "Missing access token"},
    )
