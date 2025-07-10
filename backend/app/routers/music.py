from fastapi import APIRouter
from fastapi.responses import FileResponse
from ..models import MusicRequest, MusicResponse
from ..services.music_generator import MusicService

router = APIRouter(prefix="/music", tags=["music"])


@router.post("", response_model=MusicResponse)
async def create_music(req: MusicRequest) -> MusicResponse:
    path = MusicService.generate(req.mood, req.duration_sec)
    return MusicResponse(url=f"/static/{path.relative_to('static')}")
