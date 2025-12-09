import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI,Request
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin

from app.admin.views import BookingsAdmin, UsersAdmin
from app.config import settings
from app.database import engine
from app.frontend.images.router import router as images_router
from app.frontend.pages.router import router as frontend_router
from app.models.bookings.router import router as bookings_router
from app.models.hotels.rooms.router import router as room_router
from app.models.hotels.router import router as hotel_router
from app.models.users.router import router as user_router
from app.logger import logger

BASE_DIR = Path(__file__).resolve().parent
static_dir = BASE_DIR / "frontend" / "static"

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield

app = FastAPI(lifespan=lifespan)

app.mount(
    "/static",
    StaticFiles(directory=str(static_dir)),
    name="static",
)

app.include_router(user_router)
app.include_router(hotel_router)
app.include_router(room_router)
app.include_router(bookings_router)
app.include_router(frontend_router)
app.include_router(images_router)


admin = Admin(app, engine)

admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    logger.info(f"Process time: {round(process_time, 4)}")
    return response

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
