from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from app.database import get_session
from app.exceptions import IncorrectEmailOrPasswordException, UserAlreadyExistsException
from app.models.users.auth import (
    authenticate_user,
    create_access_token,
    get_password_hash,
)
from app.models.users.dependencies import get_current_user
from app.models.users.models import Users
from app.models.users.schemas import SUserAuth
from app.models.users.service import UsersService

router = APIRouter(prefix="/auth", tags=["Аутентификация"])


@router.post("/register")
async def register_user(
    user_date: SUserAuth, session: AsyncSession = Depends(get_session)
):
    existing_user = await UsersService.find_one_or_none(session, email=user_date.email)
    if existing_user:
        raise UserAlreadyExistsException

    hashed_password = get_password_hash(user_date.password)
    await UsersService.add(session, email=user_date.email, password=hashed_password)


@router.post("/login")
async def login_user(
    response: Response,
    user_date: SUserAuth,
    session: AsyncSession = Depends(get_session),
):
    user = await authenticate_user(user_date.email, user_date.password, session)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(key="booking_access_token", value=access_token, httponly=True)
    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie(key="booking_access_token")


@router.get("/me")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user
