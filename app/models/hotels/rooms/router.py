from datetime import date

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models.hotels.rooms.schemas import SRoomsWithRoomsLeftAndTotalCost
from app.models.hotels.rooms.service import RoomsService
from app.models.hotels.router import router


@router.get("/{hotel_id}/rooms", response_model=list[SRoomsWithRoomsLeftAndTotalCost])
async def get_rooms(
    hotel_id: int,
    date_from: date,
    date_to: date,
    session: AsyncSession = Depends(get_session),
) -> list[SRoomsWithRoomsLeftAndTotalCost]:
    return await RoomsService.get_rooms_with_left_and_total_cost(
        session=session,
        hotel_id=hotel_id,
        date_from=date_from,
        date_to=date_to,
    )
