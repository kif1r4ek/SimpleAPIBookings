import asyncio
import json
from datetime import datetime
from pathlib import Path

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.dialects.mysql import insert

from app.config import settings
from app.database import Base, SessionFactory, engine
from app.main import app as fastapi_app
from app.models.bookings.models import Bookings
from app.models.hotels.models import Hotels
from app.models.hotels.rooms.models import Rooms
from app.models.users.models import Users

BASE_DIR = Path(__file__).resolve().parent

def open_mock_json(model: str):
    path = BASE_DIR / f"mock_{model}.json"
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)

@pytest_asyncio.fixture(autouse=True, scope="session")
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


    hotels_mock = open_mock_json("hotels")
    rooms_mock = open_mock_json("rooms")
    users_mock = open_mock_json("users")
    bookings_mock = open_mock_json("bookings")

    for booking in bookings_mock:
        booking["date_from"] = datetime.strptime(booking["date_from"], "%Y-%m-%d")
        booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%m-%d")


    async with SessionFactory() as session:
        await session.execute(insert(Hotels).values(hotels_mock))
        await session.execute(insert(Rooms).values(rooms_mock))
        await session.execute(insert(Users).values(users_mock))
        await session.execute(insert(Bookings).values(bookings_mock))

        await session.commit()


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
async def async_client():
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as aclient:
        yield aclient


@pytest.fixture(scope="function")
async def session():
    async with SessionFactory() as session:
        yield session

# @pytest.fixture(scope="function", autouse=True)
# async def cleanup_users_table():
#     """
#     Перед КАЖДЫМ тестом очищаем таблицу users в тестовой БД
#     и сбрасываем id.
#     """
#     async with SessionFactory() as session:
#         await session.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE"))
#         await session.commit()
#         yield