from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
import src.controller
from config import PATH

router = APIRouter(
    tags=["Base"]
)


@router.get("/",
            description="Простая отправка страницы сайта")
async def get_home_page(request: Request):
    templates = Jinja2Templates(directory=PATH / "src/frontend/webpage")
    return templates.TemplateResponse("/index.html", {'request': request})


@router.get("/get_list",
             description="Получение списка лекций комнаты")
async def get_list(url_room: str):
    print(url_room)
    x= src.controller.get_list_lecture(url_room)
    print(x)
    return x

@router.get("/get_lecture",
            description="Получение материалов лекции")
async def get_lecture(url_lecture:str):
    print("HUI: ", url_lecture)
    print("123123123123")
    path = src.controller.handler_lecture(url_lecture=url_lecture)
    return FileResponse(path=path, filename="conspect.pdf")
