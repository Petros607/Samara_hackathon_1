from fastapi import APIRouter

router = APIRouter(
    tags=["Base"]
)


@router.get("/",
            description="Простая отправка страницы сайта")
@router.get("/home",
            description="Простая отправка страницы сайта")
async def get_home_page():
    return "Home page"


@router.post("/post_url",
             description="Получение url-ссылки лекции")
async def post_url():
    return "url"

@router.get("/download_file/{id_pdf}",
            description="Скачивание документа PDF по id")
async def download_file(id_pdf):
    return "file"

@router.get("/list_pdf",
            description="Отправка списка похожих pdf по названию предмета, педагогу")
async def get_list_pdf(file_name, teacher):
    return {"file_name": file_name, "teacher": teacher}
