import asyncio
from backend.app.services.prompt_generator import generate_prompts


def test_prompt_generator_basic():
    prompts = asyncio.run(generate_prompts(["猫", "霓虹", "赛博"]))
    assert 5 <= len(prompts) <= 20
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)
