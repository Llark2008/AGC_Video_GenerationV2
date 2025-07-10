from __future__ import annotations

import asyncio
from pathlib import Path
from typing import List
from diffusers import DiffusionPipeline, AutoencoderKL
import torch
from ..config import get_settings
from .lora_manager import get_lora_path
from rich import print

settings = get_settings()

CHECKPOINT = "cagliostrolab/animagine-xl-4.0"
CACHE_DIR = settings.model_dir


class ImageGenerator:
    """单例 GPU pipeline"""

    _pipe: DiffusionPipeline | None = None

    @classmethod
    def _load_base(cls) -> DiffusionPipeline:
        print("[ImageGen] loading base pipeline …")
        pipe = DiffusionPipeline.from_pretrained(
            CHECKPOINT,
            torch_dtype=torch.float16,
            variant="fp16",
            cache_dir=CACHE_DIR,
        )
        # MPS 需要 attention slicing + VAE tiling
        pipe.enable_attention_slicing()
        pipe.enable_vae_tiling()
        # 4‑bit VAE 减显存（可选）
        pipe.vae = AutoencoderKL.from_pretrained(
            CHECKPOINT, subfolder="vae", torch_dtype=torch.float16, cache_dir=CACHE_DIR
        )
        pipe.to(settings.device)
        pipe.set_progress_bar_config(disable=True)
        return pipe

    @classmethod
    def get(cls) -> DiffusionPipeline:
        if cls._pipe is None:
            cls._pipe = cls._load_base()
        return cls._pipe

    @classmethod
    async def generate(
        cls,
        prompts: List[str],
        width: int = settings.image_width,
        height: int = settings.image_height,
        lora: str | None = None,
    ) -> List[Path]:
        pipe = cls.get()

        # 应用 (单一) LoRA
        if lora:
            lora_path = get_lora_path(lora)
            pipe.load_lora_weights(lora_path, adapter_name="current")
            pipe.set_adapters(["current"], adapter_weights=[1.0])
        else:
            pipe.set_adapters([], [])  # 移除

        results: list[Path] = []
        for i, prompt in enumerate(prompts):
            print(f"[ImageGen] {i+1}/{len(prompts)} {prompt[:60]}...")
            image = await asyncio.to_thread(
                pipe,
                prompt,
                num_inference_steps=25,
                width=width,
                height=height,
            )
            out_path = Path(f"static/images/{prompt[:40].replace(' ', '_')}_{i}.png")
            out_path.parent.mkdir(parents=True, exist_ok=True)
            image.images[0].save(out_path)
            results.append(out_path)

        return results
