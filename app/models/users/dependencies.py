from datetime import datetime, timezone

from fastapi import Depends
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from app.config import settings
from app.database import get_session
from app.exceptions import (
    AccessTokenCookieMissingException,
    AccessTokenExpiredException,
    InvalidAccessTokenException,
    TokenExpInvalidTypeException,
    TokenNoExpClaimException,
    TokenNoSubClaimException,
    TokenSubNotIntegerException,
    UserNotFoundOrInactiveException,
)
from app.models.users.service import UsersService


def get_access_token(request: Request) -> str:
    token = request.cookies.get("booking_access_token")
    if not token:
        raise AccessTokenCookieMissingException
    return token


async def get_current_user(
    token: str = Depends(get_access_token),
    session: AsyncSession = Depends(get_session),
):
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_exp": True},
        )
    except ExpiredSignatureError:
        raise AccessTokenExpiredException
    except JWTError:
        raise InvalidAccessTokenException

    exp = payload.get("exp")
    if exp is None:
        raise TokenNoExpClaimException
    try:
        exp_int = int(exp)
    except (TypeError, ValueError):
        raise TokenExpInvalidTypeException
    if int(datetime.now(timezone.utc).timestamp()) >= exp_int:
        raise AccessTokenExpiredException

    user_id = payload.get("sub")
    if user_id is None:
        raise TokenNoSubClaimException
    try:
        user_id_int = int(user_id)
    except ValueError:
        raise TokenSubNotIntegerException

    user = await UsersService.find_by_id(session, user_id_int)
    if not user:
        raise UserNotFoundOrInactiveException

    return user
