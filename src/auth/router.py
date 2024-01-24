from fastapi import APIRouter, Depends, Cookie, HTTPException, Response
from fastapi.openapi.models import OAuth2
from fastapi.security import OAuth2PasswordRequestForm


from src.auth.dependencies import user_service
from src.services.user import UserServices
from src.auth.cockies import OAuth2PasswordBearerWithCookie
from src.database import get_async_session
from src.auth.jwt import create_jwt, verify_jwt
from src.auth.models import User

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from typing import Annotated

auth_rouret = APIRouter(prefix='/auth', tags=['Авторизация и регистрация'])
oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/auth/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# @user_router.get('/')
# async def get_users(user_services: Annotated[UserServices, Depends(user_service)]):
#     users = await user_services.get_users()
#     return users


@auth_rouret.get('/me')
async def get_users(access_token: Annotated[str | None, Cookie()] = None):
    user = get_current_user(access_token)
    return [user]





def get_current_user(access_token: str):
    # token = request.cookies.get('access_token')
    
    # # if token == None:
    # #     HTTPException(status_code=400, detail='Invalid token')
    # tokens = token[2::]
    # tokens = tokens.split("'")

    decode_data = verify_jwt(access_token)
    if not decode_data:
        HTTPException(status_code=400, detail='Invalid token')

    return decode_data


@auth_rouret.post("/register")
async def register_user(username: str, password: str, db: AsyncSession = Depends(get_async_session)):
    hashed_password = pwd_context.hash(secret=password, scheme='bcrypt')
    # Сохраните пользователя в базе данных
    db.add(User(username=username, hashed_password=hashed_password))
    await db.commit()
    return {"username": username, "hashed_password": hashed_password}


# response: Response, form_data: OAuth2PasswordRequestForm = Depends()
@auth_rouret.post("/token")
async def authenticate_user(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_async_session)):
    stmt = select(User).where(User.username == form_data.username)
    user = await db.scalar(stmt)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    is_password_correct = pwd_context.verify(form_data.password, user.hashed_password)

    if not is_password_correct:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    jwt_token = create_jwt({"username": user.username})

    response.set_cookie(key="access_token", value=jwt_token, httponly=True)
    return {"access_token": jwt_token, "token_type": "bearer"}









