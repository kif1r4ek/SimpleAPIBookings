from typing import Mapping, Optional

from fastapi import HTTPException, status

WWW_AUTH_HEADER: Mapping[str, str] = {"WWW-Authenticate": "Bearer"}


class BookingException(HTTPException):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "Internal server error"
    headers: Optional[Mapping[str, str]] = None

    def __init__(
        self,
        detail: Optional[str] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> None:
        super().__init__(
            status_code=self.status_code,
            detail=detail if detail is not None else self.detail,
            headers=headers if headers is not None else self.headers,
        )


# --- Auth / Users ---

class UserAlreadyExistsException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User with that email already exists."


class IncorrectEmailOrPasswordException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect email or password"
    headers = WWW_AUTH_HEADER


# --- Token / Cookies ---

class AccessTokenCookieMissingException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Access token cookie is missing"
    headers = WWW_AUTH_HEADER


class InvalidAccessTokenException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Invalid access token"
    headers = WWW_AUTH_HEADER


class AccessTokenExpiredException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Access token has expired"
    headers = WWW_AUTH_HEADER


class TokenNoExpClaimException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token has no 'exp' claim"
    headers = WWW_AUTH_HEADER


class TokenExpInvalidTypeException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token 'exp' claim has invalid type"
    headers = WWW_AUTH_HEADER


class TokenNoSubClaimException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token has no 'sub' claim"
    headers = WWW_AUTH_HEADER


class TokenSubNotIntegerException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token 'sub' claim is not an integer"
    headers = WWW_AUTH_HEADER


class UserNotFoundOrInactiveException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "User not found or inactive"
    headers = WWW_AUTH_HEADER


class RoomCannotBeBookedException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Room can't be booked"

class BookingNotFoundException(BookingException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Booking not found"


class BookingForbiddenException(BookingException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "You cannot delete this booking"
