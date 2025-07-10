from typing import List
from pydantic import BaseModel, HttpUrl


class PromptRequest(BaseModel):
    keywords: List[str]
    n: int | None = None  # 默认为 settings.prompt_batch


class PromptResponse(BaseModel):
    prompts: List[str]


class ImageRequest(BaseModel):
    prompts: List[str]
    width: int | None = None
    height: int | None = None
    lora: str | None = None


class ImageResponse(BaseModel):
    urls: List[HttpUrl]  # 本地访问统一 /static/**


class MusicRequest(BaseModel):
    mood: str = "cinematic"
    duration_sec: int = 60


class MusicResponse(BaseModel):
    url: HttpUrl


class RenderRequest(BaseModel):
    images: List[str]  # file paths
    music: str         # file path
    title: str
    author: str


class RenderResponse(BaseModel):
    url: HttpUrl
