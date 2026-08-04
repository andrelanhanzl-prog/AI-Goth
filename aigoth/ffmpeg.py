"""Nalezení ffmpeg/ffprobe a čtení délky zvukové stopy."""

from __future__ import annotations

import json
import shutil
import subprocess
from functools import lru_cache
from pathlib import Path


class FfmpegMissing(RuntimeError):
    pass


@lru_cache(maxsize=1)
def ffmpeg_binary() -> str:
    """Vrátí cestu k ffmpeg — systémový má přednost, jinak binárka z imageio-ffmpeg."""
    found = shutil.which("ffmpeg")
    if found:
        return found
    try:
        import imageio_ffmpeg
    except ImportError as exc:  # pragma: no cover - závisí na prostředí
        raise FfmpegMissing(
            "ffmpeg nenalezen. Nainstaluj ho systémově, nebo: pip install imageio-ffmpeg"
        ) from exc
    return imageio_ffmpeg.get_ffmpeg_exe()


@lru_cache(maxsize=1)
def ffprobe_binary() -> str | None:
    """ffprobe je volitelný — bez něj čteme délku zvuku přes ffmpeg."""
    return shutil.which("ffprobe")


def audio_duration(path: str | Path) -> float:
    """Délka zvukové stopy v sekundách."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"zvuková stopa neexistuje: {path}")

    probe = ffprobe_binary()
    if probe:
        out = subprocess.run(
            [probe, "-v", "error", "-show_format", "-of", "json", str(path)],
            capture_output=True,
            text=True,
            check=True,
        )
        return float(json.loads(out.stdout)["format"]["duration"])

    # Fallback: ffmpeg dekóduje do /dev/null a na stderr ohlásí dosažený čas.
    out = subprocess.run(
        [ffmpeg_binary(), "-i", str(path), "-f", "null", "-"],
        capture_output=True,
        text=True,
    )
    stamp = None
    for token in out.stderr.split():
        if token.startswith("time="):
            stamp = token[len("time=") :].strip(",")
    if stamp is None:
        raise RuntimeError(f"nepodařilo se zjistit délku stopy: {path}")
    hours, minutes, seconds = stamp.split(":")
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)
