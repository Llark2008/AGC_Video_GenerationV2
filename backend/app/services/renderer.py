from __future__ import annotations

from pathlib import Path
from typing import List
import random
from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    concatenate_videoclips,
    CompositeVideoClip,
    vfx,
)
from ..config import get_settings
from rich import print
import numpy as np

settings = get_settings()


def _ken_burns_effect(img_path: str, duration: int) -> ImageClip:
    """简易 Ken Burns：随机放缩 & 平移"""
    clip = ImageClip(img_path).resize(height=1080)
    w, h = clip.size
    zoom = random.uniform(1.05, 1.15)
    x_move = random.randint(-int(0.05 * w), int(0.05 * w))
    y_move = random.randint(-int(0.05 * h), int(0.05 * h))
    return (
        clip.fx(vfx.crop, x_center=w / 2, y_center=h / 2, width=w, height=h)
        .resize(lambda t: 1 + (zoom - 1) * (t / duration))
        .set_position(lambda t: (x_move * (t / duration), y_move * (t / duration)))
        .set_duration(duration)
    )


def render_video(images: List[str], music: str, title: str, author: str) -> Path:
    sec_per_img = settings.ken_burns_sec
    clips = [_ken_burns_effect(p, sec_per_img) for p in images]

    print("[Render] adding crossfade transitions")
    clips_with_trans = [
        clips[i].crossfadein(1) if i else clips[i] for i in range(len(clips))
    ]
    video = concatenate_videoclips(clips_with_trans, method="compose")

    # BGM
    audio = AudioFileClip(music).audio
    audio = audio.set_duration(video.duration)
    video = video.set_audio(audio)

    # 片头片尾（文字）
    txt_clip = (
        ImageClip(np.zeros((200, 1920, 3)) + 255)
        .set_duration(2)
        .set_opacity(0.0)
    )
    video = concatenate_videoclips([txt_clip, video])

    out_path = Path(f"static/videos/{title.replace(' ', '_')}.mp4")
    out_path.parent.mkdir(exist_ok=True, parents=True)
    video.write_videofile(
        out_path.as_posix(),
        fps=settings.video_fps,
        codec="libx264",
        audio_codec="aac",
        threads=4,
        preset="fast",
        logger=None,
    )
    return out_path
