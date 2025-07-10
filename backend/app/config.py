from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # 基础
    app_name: str = "AI Video"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # 外部服务
    redis_url: str = Field("redis://localhost:6379/0", alias="REDIS_URL")

    # 模型 & 权限
    openrouter_key: str | None = Field(None, alias="OPENROUTER_API_KEY")
    hf_token: str | None = Field(None, alias="HF_TOKEN")
    model_dir: Path | None = Field(None, alias="MODEL_DIR")

    # LoRA
    lora_root: Path = Path("./lora")

    # 运行参数
    device: str = "mps"  # 统一使用 mps，检测失败会 warn & 回退 cpu
    prompt_batch: int = 20
    image_width: int = 768
    image_height: int = 768
    video_fps: int = 30
    ken_burns_sec: int = 5

    # n‑gram 去重阈值
    dedup_threshold: float = 0.9


@lru_cache
def get_settings() -> Settings:
    return Settings()
