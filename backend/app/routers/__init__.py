from fastapi import APIRouter
from .prompts import router as prompt_router
from .images import router as image_router
from .music import router as music_router
from .render import router as render_router
from .lora import router as lora_router

api_router = APIRouter()
api_router.include_router(prompt_router)
api_router.include_router(image_router)
api_router.include_router(music_router)
api_router.include_router(render_router)
api_router.include_router(lora_router)
