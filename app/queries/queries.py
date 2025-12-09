from datetime import date

from sqlalchemy import and_, func, select

from app.models.bookings.models import Bookings
from app.models.hotels.rooms.models import Rooms


def rooms_left_per_room(date_from: date, date_to: date):
    overlap = and_(
        Bookings.date_from < date_to,  # начало брони строго до конца периода
        Bookings.date_to > date_from,  # конец брони строго после начала периода
    )

    get_rooms_left = (
        select(
            Rooms.id.label("room_id"),
            Rooms.hotel_id.label("hotel_id"),
            (Rooms.quantity - func.count(Bookings.id)).label("rooms_left"),
        )
        .select_from(Rooms)
        .join(
            Bookings,
            and_(Bookings.room_id == Rooms.id, overlap),
            isouter=True,
        )
        .group_by(Rooms.id, Rooms.hotel_id, Rooms.quantity)
        .cte("rooms_left_per_room")
    )

    return get_rooms_left
