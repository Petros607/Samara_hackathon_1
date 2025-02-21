from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pathlib
from config import PATH


def generate_html_response(path: str) -> HTMLResponse:
    # "src/frontend/webpage/index.html"

    with open(PATH / path, "r") as html_file:
        html_content = html_file.readlines()

    return HTMLResponse(content=html_content, status_code=200)
