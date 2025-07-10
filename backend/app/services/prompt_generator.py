import random
import httpx
from .dedup import deduplicate
from ..config import get_settings
from rich import print

settings = get_settings()

LOCAL_MODEL = "microsoft/phi-3-mini-4k-instruct"


async def _call_openrouter(prompt: str) -> list[str]:
    """调用 OpenRouter，返回纯文本行列表"""
    headers = {
        "Authorization": f"Bearer {settings.openrouter_key}",
        "HTTP-Referer": "https://github.com/your/repo",
    }
    body = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 400,
        "temperature": 1.0,
        "top_p": 0.95,
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post("https://openrouter.ai/api/v1/chat/completions", json=body, headers=headers, timeout=30)
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]
    lines = [l.strip("- ").strip() for l in content.splitlines() if l.strip()]
    return lines


async def generate_prompts(keywords: list[str], n: int | None = None) -> list[str]:
    n = n or settings.prompt_batch
    seed = ", ".join(keywords)
    system_prompt = (
        "You are an imaginative prompt generator for text-to-image diffusion models. "
        "Return each prompt on a new line, exactly N lines."
    )
    user_prompt = f"Generate {n} rich, cinematic style English prompts based on: {seed}."
    try:
        if settings.openrouter_key:
            lines = await _call_openrouter(f"{system_prompt}\n{user_prompt}")
        else:
            raise RuntimeError("OpenRouter KEY missing, fallback to local")
    except Exception as exc:  # noqa: BLE001
        print(f"[PromptGen] remote failed: {exc}, fallback to simple")
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer
            import torch

            tok = AutoTokenizer.from_pretrained(LOCAL_MODEL, trust_remote_code=True)
            mdl = AutoModelForCausalLM.from_pretrained(
                LOCAL_MODEL,
                torch_dtype="auto",
                trust_remote_code=True,
                device_map=settings.device,
            )
            prompt_ids = tok.encode(
                f"{system_prompt}\n{user_prompt}", return_tensors="pt"
            ).to(settings.device)
            streamer = TextStreamer(tok)
            out = mdl.generate(
                prompt_ids,
                max_new_tokens=512,
                temperature=1.0,
                top_p=0.95,
                streamer=streamer,
            )
            text = tok.decode(out[0], skip_special_tokens=True)
            lines = [l.strip("- ").strip() for l in text.splitlines() if l.strip()]
        except Exception as inner_exc:  # noqa: BLE001
            print(f"[PromptGen] local model unavailable: {inner_exc}")
            # Extremely simple fallback using the keywords
            lines = [f"{seed} scene {i}" for i in range(1, n + 1)]
    # 去重 & 截取前 n 行
    return deduplicate(lines)[:n]
