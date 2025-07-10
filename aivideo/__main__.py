import json
from pathlib import Path
import typer
import asyncio
from backend.app.services.prompt_generator import generate_prompts
from backend.app.services.image_generator import ImageGenerator
from backend.app.services.music_generator import MusicService
from backend.app.services.renderer import render_video

cli = typer.Typer(help="AI 二创视频自动生成工具 CLI")


@cli.command()
def run(
    keywords_file: Path = typer.Argument(..., exists=True),
    output: Path = typer.Option("cli_output.mp4", "--out", "-o"),
):
    """
    一键离线生成示例作品：读取 keywords.txt，
    依次走 Prompt→图像→音乐→合成，耗时 ~10 分钟（首次模型加载更久）。
    """
    keywords = [k.strip() for k in keywords_file.read_text().splitlines() if k.strip()]
    prompts = asyncio.run(generate_prompts(keywords))
    images = asyncio.run(ImageGenerator.generate(prompts[:10]))  # 前 10 张即可
    music = MusicService.generate(mood="cinematic", duration=60)
    video = render_video([p.as_posix() for p in images], music.as_posix(), "CLI Demo", "aivideo")
    Path(output).write_bytes(Path(video).read_bytes())
    typer.echo(f"[+] 完成！结果位于 {output}")


def _main():
    cli()


if __name__ == "__main__":
    _main()
