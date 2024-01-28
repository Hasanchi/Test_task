from fastapi import APIRouter, Depends, HTTPException, Response, Request
from fastapi.security import OAuth2PasswordRequestForm

from src.database import get_async_session
from src.user.jwt import create_jwt, verify_jwt
from src.models import User

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

user_router = APIRouter(prefix='/user', tags=['Пользователь'])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_current_user(request: Request):
    access_token = request.cookies.get('access_token')
    decode_data = verify_jwt(access_token)
    if decode_data is None:
        HTTPException(status_code=400, detail='Invalid token')
    return decode_data


@user_router.put('/me')
async def update_me(
        request: Request,
        username: str,
        password: str,
        session: AsyncSession = Depends(get_async_session)
):
    decode_data = get_current_user(request)
    user_id = decode_data['id']
    hashed_password = pwd_context.hash(secret=password, scheme='bcrypt')
    query = (
        update(User)
        .values(
            username=username,
            hashed_password=hashed_password
        ).where(User.id == user_id)
    )
    await session.execute(query)
    await session.commit()
    return {
        'message': 'Ваши данные успешно изменены'
    }


@user_router.post("/register")
async def register_user(
        username: str,
        password: str,
        db: AsyncSession = Depends(get_async_session)
):
    hashed_password = pwd_context.hash(secret=password, scheme='bcrypt')
    db.add(User(username=username, hashed_password=hashed_password))
    await db.commit()
    return {"username": username, "hashed_password": hashed_password}


@user_router.post("/token")
async def authenticate_user(
        response: Response,
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_async_session)
):
    stmt = select(User).where(User.username == form_data.username)
    user = await db.scalar(stmt)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Пользователь не найден"
        )

    is_password_correct = pwd_context.verify(
        form_data.password,
        user.hashed_password
    )

    if not is_password_correct:
        raise HTTPException(
            status_code=400,
            detail="Некорректный password или username"
        )

    jwt_token = create_jwt(
                {
                    "id": user.id,
                    "username": user.username
                }
            )

    response.set_cookie(key="access_token", value=jwt_token, httponly=True)
    return {"access_token": jwt_token, "token_type": "bearer"}
