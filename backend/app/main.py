from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routers import api_router
from .config import get_settings
from rich import print

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
)

app.include_router(api_router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def _init_models() -> None:
    print("[Startup] backend ready — you can now POST /prompts etc.")
