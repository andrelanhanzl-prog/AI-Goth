#!/usr/bin/env python3
"""Vygeneruje záběry filmu KONEC CYKLU přes Gemini / Veo.

Použití:
    pip install google-genai
    export GEMINI_API_KEY=...
    python scripts/generate_video.py                 # všech 8 záběrů
    python scripts/generate_video.py --shots 5 8     # jen vybrané
    python scripts/generate_video.py --chain         # navazuj přes poslední snímek

Výstup: out/shot_01.mp4 ... out/shot_08.mp4 — sestříhej v pořadí (viz --ffmpeg).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

from google import genai
from google.genai import types

ROOT = Path(__file__).resolve().parent.parent
PROMPT_FILE = ROOT / "prompts" / "cyklus_veo_prompt.json"
OUT_DIR = ROOT / "out"

MODEL = os.environ.get("VEO_MODEL", "veo-3.1-generate-preview")
POLL_SECONDS = 10


def build_prompt(shot: dict, style: dict) -> str:
    """Slepí popis záběru s globálním stylem do jednoho promptu pro Veo."""
    parts = [
        shot["prompt"],
        f"Camera: {shot['camera']}.",
        f"Lighting: {shot['lighting']}.",
        f"Audio: {shot['audio']}. No dialogue.",
        f"Style: {style['look']}.",
        f"Palette: {style['palette']}.",
        f"Grade: {style['grade']}.",
        f"Motion: {style['motion']}.",
    ]
    return "\n".join(parts)


def generate_shot(
    client: genai.Client,
    shot: dict,
    style: dict,
    out_path: Path,
    seed: int | None,
    first_frame: types.Image | None,
) -> Path:
    prompt = build_prompt(shot, style)
    config = types.GenerateVideosConfig(
        aspect_ratio="16:9",
        resolution="1080p",
        number_of_videos=1,
        negative_prompt=style["negative_prompt"],
    )
    if seed is not None:
        config.seed = seed

    print(f"[{shot['id']}] {shot['title']} — odesílám…", flush=True)
    operation = client.models.generate_videos(
        model=MODEL,
        prompt=prompt,
        image=first_frame,
        config=config,
    )

    waited = 0
    while not operation.done:
        time.sleep(POLL_SECONDS)
        waited += POLL_SECONDS
        print(f"[{shot['id']}] generuji… {waited}s", flush=True)
        operation = client.operations.get(operation)

    if operation.error:
        raise RuntimeError(f"záběr {shot['id']} selhal: {operation.error}")

    video = operation.response.generated_videos[0].video
    client.files.download(file=video)
    video.save(str(out_path))
    print(f"[{shot['id']}] hotovo → {out_path}", flush=True)
    return out_path


def main() -> int:
    ap = argparse.ArgumentParser(description="KONEC CYKLU — generátor záběrů")
    ap.add_argument("--shots", type=int, nargs="*", help="ID záběrů (default: všechny)")
    ap.add_argument("--seed", type=int, default=None, help="fixní seed pro konzistenci")
    ap.add_argument(
        "--chain",
        action="store_true",
        help="použij poslední snímek předchozího klipu jako vstup dalšího (image-to-video)",
    )
    ap.add_argument("--out", type=Path, default=OUT_DIR)
    ap.add_argument("--ffmpeg", action="store_true", help="na konci slep klipy do film.mp4")
    args = ap.parse_args()

    if not os.environ.get("GEMINI_API_KEY"):
        print("Chybí GEMINI_API_KEY.", file=sys.stderr)
        return 1

    spec = json.loads(PROMPT_FILE.read_text(encoding="utf-8"))
    style = spec["global_style"]
    shots = spec["shots"]
    if args.shots:
        wanted = set(args.shots)
        shots = [s for s in shots if s["id"] in wanted]
        if not shots:
            print("Žádný záběr s tímto ID.", file=sys.stderr)
            return 1

    args.out.mkdir(parents=True, exist_ok=True)
    client = genai.Client()

    written: list[Path] = []
    first_frame: types.Image | None = None
    for shot in shots:
        out_path = args.out / f"shot_{shot['id']:02d}.mp4"
        written.append(
            generate_shot(client, shot, style, out_path, args.seed, first_frame)
        )
        if args.chain:
            first_frame = extract_last_frame(out_path, args.out)

    if args.ffmpeg and written:
        concat_clips(written, args.out / "film.mp4")

    print(f"\nHotovo: {len(written)} záběrů v {args.out}")
    return 0


def extract_last_frame(clip: Path, out_dir: Path) -> types.Image:
    """Vytáhne poslední snímek klipu jako vstupní obrázek pro navazující záběr."""
    import subprocess

    frame = out_dir / f"{clip.stem}_last.png"
    subprocess.run(
        ["ffmpeg", "-y", "-sseof", "-0.1", "-i", str(clip), "-frames:v", "1", str(frame)],
        check=True,
        capture_output=True,
    )
    return types.Image(image_bytes=frame.read_bytes(), mime_type="image/png")


def concat_clips(clips: list[Path], target: Path) -> None:
    """Slepí klipy za sebe bez rekomprese."""
    import subprocess

    listing = target.parent / "concat.txt"
    listing.write_text("".join(f"file '{c.name}'\n" for c in clips), encoding="utf-8")
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listing), "-c", "copy", str(target)],
        check=True,
    )
    print(f"Film sestříhán → {target}")


if __name__ == "__main__":
    raise SystemExit(main())
