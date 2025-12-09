import asyncio
from datetime import date

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models.hotels.schemas import SHotelWithRoomsLeft
from app.models.hotels.service import HotelsService

router = APIRouter(
    prefix="/hotels", tags=["Отели"], responses={404: {"description": "Not found"}}
)


@router.get("/{location}", response_model=list[SHotelWithRoomsLeft])
@cache(expire=60)
async def get_hotels(
    location: str,
    date_from: date,
    date_to: date,
    session: AsyncSession = Depends(get_session),
) -> list[SHotelWithRoomsLeft]:
    await asyncio.sleep(3)
    return await HotelsService.get_filter_hotels(
        location=location, date_from=date_from, date_to=date_to, session=session
    )
