from fastapi import APIRouter
from ..models import RenderRequest, RenderResponse
from ..services.renderer import render_video

router = APIRouter(prefix="/render", tags=["render"])


@router.post("", response_model=RenderResponse)
async def render(req: RenderRequest) -> RenderResponse:
    path = render_video(req.images, req.music, req.title, req.author)
    return RenderResponse(url=f"/static/{path.relative_to('static')}")
