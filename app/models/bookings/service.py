from datetime import date

from sqladmin.exceptions import SQLAdminException
from sqlalchemy import select
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import BookingForbiddenException, BookingNotFoundException
from app.logger import logger
from app.models.bookings.models import Bookings
from app.models.bookings.schemas import SBookingWithRoom
from app.models.hotels.rooms.models import Rooms
from app.queries.queries import rooms_left_per_room
from app.service.base import BaseService


class BookingsService(BaseService):
    model = Bookings

    try:
        @classmethod
        async def add_bookings(
            cls,
            session: AsyncSession,
            user_id: int,
            room_id: int,
            date_from: date,
            date_to: date,
        ):
            rooms_left = rooms_left_per_room(date_from, date_to)

            rooms_left_stmt = select(rooms_left.c.rooms_left).where(
                rooms_left.c.room_id == room_id
            )
            rooms_left = await session.scalar(rooms_left_stmt)
            if rooms_left is None or rooms_left <= 0:
                return None

            price_stmt = select(Rooms.price).where(Rooms.id == room_id)
            price = await session.scalar(price_stmt)
            if price is None:
                return None

            insert_stmt = (
                insert(Bookings)
                .values(
                    user_id=user_id,
                    room_id=room_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price,
                )
                .returning(Bookings)
            )

            new_booking = await session.scalar(insert_stmt)
            await session.commit()
            return new_booking

        @classmethod
        async def find_user_bookings_with_room(
            cls,
            session: AsyncSession,
            user_id: int,
        ) -> list[SBookingWithRoom]:
            stmt = (
                select(
                    Bookings.id,
                    Bookings.room_id,
                    Bookings.user_id,
                    Bookings.date_from,
                    Bookings.date_to,
                    Bookings.price,
                    Bookings.total_days,
                    Bookings.total_cost,
                    Rooms.image_id,
                    Rooms.name,
                    Rooms.description,
                    Rooms.service.label("services"),  # колонка service -> ключ services
                )
                .join(Rooms, Rooms.id == Bookings.room_id)
                .where(Bookings.user_id == user_id)
            )

            result = await session.execute(stmt)
            rows = result.mappings().all()

            return [SBookingWithRoom(**row) for row in rows]

        @classmethod
        async def delete_bookings(
            cls, session: AsyncSession, booking_id: int, user_id: int
        ) -> None:
            booking = await cls.find_by_id(session, booking_id)

            if booking is None:
                raise BookingNotFoundException()

            if booking.user_id != user_id:
                raise BookingForbiddenException()

            await session.delete(booking)
            await session.commit()
    except (SQLAlchemyError, Exception) as e:
        msg = ""
        if isinstance(e, SQLAlchemyError):
            msg = "Database Exe"
        elif isinstance(e, Exception):
            msg = "Unknown Exe"

        msg += ": Cannot add booking"

        logger.error(
            msg,
            exc_info=True,
        )
