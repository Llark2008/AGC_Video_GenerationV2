from fastapi import APIRouter
from fastapi.responses import FileResponse
from ..models import ImageRequest, ImageResponse
from ..services.image_generator import ImageGenerator

router = APIRouter(prefix="/images", tags=["images"])


@router.post("", response_model=ImageResponse)
async def create_images(req: ImageRequest) -> ImageResponse:
    paths = await ImageGenerator.generate(
        req.prompts,
        width=req.width or 768,
        height=req.height or 768,
        lora=req.lora,
    )
    urls = [f"/static/{p.relative_to('static')}" for p in paths]
    return ImageResponse(urls=urls)
