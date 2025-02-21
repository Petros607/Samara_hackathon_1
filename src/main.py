from fastapi import FastAPI

from src.router import router as router_base

app = FastAPI()

app.include_router(router_base)
