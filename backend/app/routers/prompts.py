from fastapi import APIRouter, Depends
from ..models import PromptRequest, PromptResponse
from ..services.prompt_generator import generate_prompts
from ..config import get_settings

router = APIRouter(prefix="/prompts", tags=["prompts"])
settings = get_settings()


@router.post("", response_model=PromptResponse)
async def create_prompts(payload: PromptRequest) -> PromptResponse:
    prompts = await generate_prompts(payload.keywords, payload.n or settings.prompt_batch)
    return PromptResponse(prompts=prompts)
