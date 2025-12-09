from datetime import date

from pydantic import BaseModel, ConfigDict


class SBookings(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_days: int
    total_cost: int

    model_config = ConfigDict(from_attributes=True)


class SBookingWithRoom(SBookings):
    image_id: int  # из Rooms
    name: str  # из Rooms
    description: str  # из Rooms
    services: list[str]  # из Rooms.service (JSONB)
