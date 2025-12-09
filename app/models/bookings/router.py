from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.database import get_session
from app.exceptions import RoomCannotBeBookedException
from app.models.bookings.schemas import SBookings, SBookingWithRoom
from app.models.bookings.service import BookingsService
from app.models.users.dependencies import get_current_user
from app.models.users.models import Users
from app.tasks.tasks import send_booking_confirmation_email

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=list[SBookingWithRoom])
async def get_bookings(
    user: Users = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> list[SBookingWithRoom]:
    return await BookingsService.find_user_bookings_with_room(
        session=session,
        user_id=user.id,
    )


@router.post("", response_model=SBookings)
async def add_booking(
    room_id: int,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    booking = await BookingsService.add_bookings(
        session=session,
        user_id=user.id,
        room_id=room_id,
        date_from=date_from,
        date_to=date_to,
    )

    if not booking:
        raise RoomCannotBeBookedException()

    booking_schema = SBookings.model_validate(
        booking,
        from_attributes=True,
    )

    send_booking_confirmation_email.delay(
        booking_schema.model_dump(),
        user.email,
    )

    return booking_schema


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(
    booking_id: int,
    user: Users = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> None:
    await BookingsService.delete_bookings(
        session, user_id=user.id, booking_id=booking_id
    )
