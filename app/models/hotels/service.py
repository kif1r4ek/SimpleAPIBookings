from datetime import date

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.hotels.models import Hotels
from app.models.hotels.schemas import SHotelWithRoomsLeft
from app.queries.queries import rooms_left_per_room
from app.service.base import BaseService


class HotelsService(BaseService):
    model = Hotels

    @classmethod
    async def get_filter_hotels(
        cls, location: str, date_from: date, date_to: date, session: AsyncSession
    ) -> list[SHotelWithRoomsLeft]:
        rooms_left_cte = rooms_left_per_room(date_from, date_to)

        stmt = (
            select(
                Hotels.id,
                Hotels.name,
                Hotels.location,
                Hotels.service,
                Hotels.rooms_quantity,
                Hotels.image_id,
                func.sum(rooms_left_cte.c.rooms_left).label("rooms_left"),
            )
            .join(rooms_left_cte, rooms_left_cte.c.hotel_id == Hotels.id)
            .where(
                or_(
                    Hotels.location.ilike(f"%{location}%"),
                    Hotels.name.ilike(f"%{location}%"),
                )
            )
            .group_by(
                Hotels.id,
                Hotels.name,
                Hotels.location,
                Hotels.service,
                Hotels.rooms_quantity,
                Hotels.image_id,
            )
            .having(func.sum(rooms_left_cte.c.rooms_left) > 0)
        )

        result = await session.execute(stmt)
        rows = result.mappings().all()

        return [SHotelWithRoomsLeft(**row) for row in rows]
