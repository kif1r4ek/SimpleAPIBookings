from datetime import date

from sqlalchemy import literal, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.hotels.rooms.models import Rooms
from app.models.hotels.rooms.schemas import SRoomsWithRoomsLeftAndTotalCost
from app.queries.queries import rooms_left_per_room
from app.service.base import BaseService


class RoomsService(BaseService):
    model = Rooms

    @classmethod
    async def get_rooms_with_left_and_total_cost(
        cls,
        session: AsyncSession,
        hotel_id: int,
        date_from: date,
        date_to: date,
    ) -> list[SRoomsWithRoomsLeftAndTotalCost]:
        nights = (date_to - date_from).days
        if nights <= 0:
            raise ValueError("date_to должен быть позже date_from")

        # берём уже готовый CTE
        rooms_left_cte = rooms_left_per_room(date_from, date_to)

        stmt = (
            select(
                Rooms.id,
                Rooms.hotel_id,
                Rooms.name,
                Rooms.description,
                Rooms.service.label("services"),
                Rooms.price,
                Rooms.quantity,
                Rooms.image_id,
                (Rooms.price * literal(nights)).label("total_cost"),
                rooms_left_cte.c.rooms_left,
            )
            .join(rooms_left_cte, rooms_left_cte.c.room_id == Rooms.id)
            .where(
                Rooms.hotel_id == hotel_id,
                rooms_left_cte.c.rooms_left > 0,
            )
        )

        result = await session.execute(stmt)
        rows = result.mappings().all()

        return [SRoomsWithRoomsLeftAndTotalCost(**row) for row in rows]
