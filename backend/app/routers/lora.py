from fastapi import APIRouter
from ..services.lora_manager import list_lora

router = APIRouter(prefix="/lora", tags=["lora"])


@router.get("/list")
def list_available() -> list[str]:
    return list_lora()
