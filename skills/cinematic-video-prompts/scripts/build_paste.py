#!/usr/bin/env python3
"""Merge a scenario file into self-contained, paste-ready shot prompts.

Hand-merging a global style block into ten shots is where packages drift apart:
one shot ends up with a different palette, and the film stops looking like a film.
This does the merge mechanically instead.

Input scenario JSON:

    {
      "film": {"title": "...", "logline": "...", "clip_seconds": 8},
      "global_style": {
        "style": "cinematic 35mm anamorphic, shallow depth of field, film grain",
        "palette": "vacuum black, ember orange, bone white, cold cyan",
        "avoid": "text, subtitles, watermarks, logos, interface elements"
      },
      "shots": [
        {"id": 1, "title": "...", "prompt": "...", "camera": "...",
         "lighting": "...", "audio": "...",
         "skip_global": false, "extra_avoid": "humanoid robot cliche"}
      ]
    }

Every field except `prompt` is optional. `skip_global` drops the shared style and
palette for a shot that deliberately breaks the look — the one moment a palette
break is worth more than consistency.

Usage:
    python build_paste.py scenario.json -o GEMINI_PASTE.json
    python build_paste.py scenario.json --shot 5      # print one prompt
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def compose(shot: dict, style: dict) -> str:
    """Build one standalone prompt string. Order matters: subject first — models
    weight the opening of the prompt most heavily — then craft, then exclusions."""
    parts = [shot["prompt"].strip()]

    for key, label in (("camera", "Camera"), ("lighting", "Lighting")):
        if shot.get(key):
            parts.append(f"{label}: {shot[key].strip().rstrip('.')}.")

    if not shot.get("skip_global"):
        for key, label in (("style", "Style"), ("palette", "Palette")):
            if style.get(key):
                parts.append(f"{label}: {style[key].strip().rstrip('.')}.")

    if shot.get("audio"):
        audio = shot["audio"].strip().rstrip(".")
        suffix = "" if "dialogue" in audio.lower() else " No dialogue."
        parts.append(f"Audio: {audio}.{suffix}")

    avoid = ", ".join(
        p.strip().rstrip(".") for p in (style.get("avoid"), shot.get("extra_avoid")) if p
    )
    if avoid:
        parts.append(f"Avoid: {avoid}.")

    return " ".join(parts)


def build(scenario: dict) -> dict:
    style = scenario.get("global_style", {})
    film = scenario.get("film", {})
    shots = scenario.get("shots", [])
    if not shots:
        raise ValueError("scenario has no shots")

    clip = film.get("clip_seconds", 8)
    out_shots = []
    for i, shot in enumerate(shots, start=1):
        if not shot.get("prompt"):
            raise ValueError(f"shot {shot.get('id', i)} has no 'prompt'")
        out_shots.append(
            {
                "id": shot.get("id", i),
                "title": shot.get("title", f"Shot {i}"),
                "paste": compose(shot, style),
            }
        )

    return {
        "_howto": (
            "Paste this whole file into the video tool and ask for one shot at a "
            "time ('Generate shot 1.'), or paste a single shot's 'paste' value on "
            "its own — each is complete and needs nothing appended. Hold the seed "
            "fixed across the piece."
        ),
        "_runtime": f"{len(out_shots)} shots x {clip}s = {len(out_shots) * clip}s",
        "film": film,
        "shots": out_shots,
        "_notes": scenario.get("notes", {}),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("scenario", type=Path)
    ap.add_argument("-o", "--out", type=Path, help="write JSON here (default: stdout)")
    ap.add_argument("--shot", type=int, help="print just this shot's prompt")
    args = ap.parse_args()

    try:
        scenario = json.loads(args.scenario.read_text(encoding="utf-8"))
        package = build(scenario)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.shot is not None:
        match = next((s for s in package["shots"] if s["id"] == args.shot), None)
        if not match:
            print(f"error: no shot with id {args.shot}", file=sys.stderr)
            return 1
        print(match["paste"])
        return 0

    text = json.dumps(package, indent=2, ensure_ascii=False)
    if args.out:
        args.out.write_text(text + "\n", encoding="utf-8")
        lengths = [len(s["paste"]) for s in package["shots"]]
        print(
            f"{args.out}: {len(package['shots'])} shots, "
            f"prompts {min(lengths)}-{max(lengths)} chars"
        )
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
