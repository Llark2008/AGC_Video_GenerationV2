from pathlib import Path
from typing import List
from ..config import get_settings

settings = get_settings()
LORA_ROOT = settings.lora_root
LORA_ROOT.mkdir(exist_ok=True)


def list_lora() -> List[str]:
    return [p.stem for p in LORA_ROOT.glob("*.safetensors")]


def get_lora_path(name: str) -> Path:
    target = LORA_ROOT / f"{name}.safetensors"
    if not target.exists():
        raise FileNotFoundError(f"LoRA {name} not found")
    return target
