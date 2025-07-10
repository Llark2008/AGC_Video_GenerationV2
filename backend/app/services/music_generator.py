from __future__ import annotations

from pathlib import Path
from typing import List
import torch
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
from ..config import get_settings
from tqdm import tqdm
from rich import print

settings = get_settings()
MODEL_NAME = "facebook/musicgen-medium"


class MusicService:
    _model: MusicGen | None = None

    @classmethod
    def _load(cls) -> MusicGen:
        print("[MusicGen] loading model…")
        model = MusicGen.get_pretrained(MODEL_NAME, device=settings.device, cache_dir=settings.model_dir)
        model.set_generation_params(top_k=250, temperature=1.0)
        return model

    @classmethod
    def get(cls) -> MusicGen:
        if cls._model is None:
            cls._model = cls._load()
        return cls._model

    @classmethod
    def generate(cls, mood: str, duration: int) -> Path:
        model = cls.get()
        wavs = model.generate([mood], progress=True, durations=[duration])
        out_path = Path(f"static/music/{mood}_{duration}s.wav")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        audio_write(out_path.with_suffix(""), wavs[0].cpu(), model.sample_rate, strategy="loudness")
        return out_path
