from fastapi import HTTPException, APIRouter, Response
from fastapi.params import Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from authx import AuthX, AuthXConfig
from api_v1.users import UserLogin
from api_v1.users.dependencies import get_current_user
from api_v1.users.schemas import UserRegister, CreateUser
from core.models import User, db_helper
from passlib.context import CryptContext
from core.config import settings
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

config = AuthXConfig()
config.JWT_ALGORITHM = "HS256"
config.JWT_SECRET_KEY = settings.SECRET_KEY
config.JWT_ACCESS_COOKIE_NAME = settings.JWT_ACCESS_COOKIE_NAME
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)


@router.post("/login")
async def login(
    credentials: UserLogin,
    db: AsyncSession = Depends(db_helper.get_db),
) -> JSONResponse:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    result = await db.execute(select(User).where(User.username == credentials.username))
    user = result.scalar_one_or_none()

    if user and pwd_context.verify(
        credentials.password,
        str(user.hashed_password),
    ):
        token = security.create_access_token(uid=str(user.id))

        response = JSONResponse(content={"access_token": token})
        response.set_cookie(
            key=config.JWT_ACCESS_COOKIE_NAME,
            value=token,
            httponly=True,
            secure=False,
            samesite="lax",
            path="/",
            max_age=3600,
        )
        return response

    raise HTTPException(
        status_code=401,
        detail="Incorrect username or password",
    )


@router.post("/register/", status_code=201)
async def register_user(
    user_data: UserRegister,
    db: AsyncSession = Depends(db_helper.get_db),
):
    user_count = await db.scalar(select(func.count(User.id)))
    if user_count > 0:
        raise HTTPException(
            status_code=403,
            detail="Initial admin already exists",
        )
    existing_user = await db.scalar(
        select(User).where(User.username == user_data.username)
    )
    if existing_user:
        raise HTTPException(status_code=409, detail="User already exists")

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    user_dict = user_data.model_dump()
    password = user_dict.pop("password")
    user_dict["hashed_password"] = pwd_context.hash(password)

    user = CreateUser(**user_dict)
    db_user = User(**user.model_dump())

    db.add(db_user)
    await db.commit()
    return {"message": "User created", "id": db_user.id}
