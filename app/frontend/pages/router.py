from fastapi import APIRouter, Request
from fastapi.params import Depends
from fastapi.templating import Jinja2Templates

from app.models.hotels.router import get_hotels

router = APIRouter(
    prefix="/pages", tags=["Фронтенд"], responses={404: {"description": "Not found"}}
)

templates = Jinja2Templates(directory="app/frontend/templates")


@router.get("/hotels")
async def get_hotels_pages(request: Request, hotels=Depends(get_hotels)):
    return templates.TemplateResponse(
        name="hotels.html", context={"request": request, "hotels": hotels}
    )
