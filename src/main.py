from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.router import router as router_base
import os
import config

app = FastAPI()

app.include_router(router_base)
app.mount("/static", StaticFiles(directory= config.PATH / "src/frontend/webpage"), name="static")
