from fastapi import FastAPI

from src.router import router as router_base
from src.ai.router import router as router_ai

app = FastAPI()

app.include_router(router_base)
app.include_router(router_ai)
