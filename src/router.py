from fastapi import APIRouter
import response

router = APIRouter(
    tags=["Base"]
)


@router.get("/",
            description="Простая отправка страницы сайта")
@router.get("/home",
            description="Простая отправка страницы сайта")
async def get_home_page():
    return response.generate_html_response("src/frontend/webpage/index.html")


@router.get("/get_list",
             description="Получение списка лекций комнаты")
async def post_url(url_room: str):
    return "list"

@router.get("/get_lecture",
            description="Отправка списка похожих files по названию предмета, педагогу")
async def get_list_pdf(url_lecture):
    return "file"