import shutil
from pathlib import Path

from fastapi import APIRouter, UploadFile

from app.tasks.tasks import process_pic

router = APIRouter(
    prefix="/images",
    tags=["Загрузка картинок"],
)

BASE_DIR = Path(__file__).resolve().parents[2]  # например: .../FastAPICources
IMG_DIR = BASE_DIR / "frontend" / "static" / "img"
IMG_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/hotels")
async def add_hotel_image(name: int, file: UploadFile):
    file_path = IMG_DIR / f"{name}.jpg"
    with open(file_path, "wb+") as f:
        shutil.copyfileobj(file.file, f)
    process_pic.delay(str(file_path))
