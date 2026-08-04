"""Zápis snímků do ffmpeg a přimixování zvukové stopy."""

from __future__ import annotations

import subprocess
from collections.abc import Callable
from pathlib import Path

from ..ffmpeg import ffmpeg_binary
from ..program import Program
from ..timeline import Timeline
from .frame import FrameRenderer


def build_command(
    program: Program,
    output: Path,
    audio: Path | None,
    crf: int,
    preset: str,
) -> list[str]:
    width, height = program.resolution
    command = [
        ffmpeg_binary(),
        "-y",
        "-loglevel", "error",
        "-f", "rawvideo",
        "-pix_fmt", "rgb24",
        "-s", f"{width}x{height}",
        "-r", str(program.fps),
        "-i", "-",
    ]
    if audio is not None:
        command += ["-i", str(audio)]
    command += [
        "-c:v", "libx264",
        "-preset", preset,
        "-crf", str(crf),
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
    ]
    if audio is not None:
        # -shortest: video i zvuk končí spolu, i když se délky o zlomek liší.
        command += ["-c:a", "aac", "-b:a", "192k", "-shortest"]
    command += [str(output)]
    return command


def render_video(
    program: Program,
    timeline: Timeline,
    output: str | Path,
    audio: str | Path | None = None,
    crf: int = 18,
    preset: str = "medium",
    on_progress: Callable[[int, int], None] | None = None,
) -> Path:
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    audio_path = Path(audio) if audio is not None else None

    renderer = FrameRenderer(program, timeline)
    total = timeline.frame_count(program.fps)
    command = build_command(program, output, audio_path, crf, preset)

    process = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    assert process.stdin is not None
    try:
        for index in range(total):
            frame = renderer.render_at(index / program.fps, frame_index=index)
            process.stdin.write(frame.tobytes())
            if on_progress is not None:
                on_progress(index + 1, total)
        process.stdin.close()
    except BrokenPipeError:
        pass  # ffmpeg spadl — skutečnou příčinu přečteme z stderr níže
    except BaseException:
        process.kill()
        raise

    stderr = process.stderr.read().decode("utf-8", "replace") if process.stderr else ""
    if process.wait() != 0:
        raise RuntimeError(f"ffmpeg selhal (kód {process.returncode}):\n{stderr.strip()}")
    return output
