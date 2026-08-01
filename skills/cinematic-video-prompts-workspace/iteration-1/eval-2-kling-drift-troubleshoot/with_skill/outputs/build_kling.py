#!/usr/bin/env python3
"""Build KLING_PASTE.json from scenario.json.

Uses the skill's build_paste.py to merge the global style block into every shot
mechanically (hand-merging is where packages drift), then adds the one thing
Kling needs that a generic package does not: a separate `negative` string per
shot. Kling has a dedicated negative-prompt box, and putting "Avoid: cartoon"
inside the main prompt tends to summon the thing you named. So the avoid list is
kept OUT of the paste string and shipped alongside it.

Usage:  python build_kling.py
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

SKILL = Path("/home/user/AI-Goth/skills/cinematic-video-prompts/scripts/build_paste.py")
HERE = Path(__file__).parent

spec = importlib.util.spec_from_file_location("build_paste", SKILL)
build_paste = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build_paste)

GLOBAL_NEGATIVE = (
    "cartoon, anime, illustration, painting, sketch, 3d render, cgi, video game, "
    "plastic skin, text, subtitles, captions, watermark, logo, timestamp, ui elements, "
    "distorted face, extra limbs, extra fingers, morphing architecture, "
    "building changing shape, warm golden grade, golden hour, sunset, daylight, "
    "blue sky, oversaturated colour, teal and orange grade, lens flare, bloom, "
    "camera shake, handheld jitter, whip pan, crash zoom, fast cuts, slow motion water, "
    "seagulls, birds"
)

EXTRA_NEGATIVE = {
    1: "rotating beam, lit lamp room, red and white stripes, tall slender lighthouse, moon, stars, town lights on shore",
    2: "wide open staircase, wooden stairs, electric wall lights, second person",
    3: "beam of light, glowing lens, working lamp, electric bulb, second person",
    4: "legible handwriting, printed text, numbers, dates, typewriter text, blank pages, hands on both sides of frame",
    5: "open crates, spilled contents, cardboard boxes, boat, harbour, more than one door",
    6: "ship close-up, large visible vessel, red and green navigation lights, deck detail, rain on lens",
    7: "second person, ghost figure, face in the reflection, mirror double, full beam sweeping, fire spreading",
    8: "amber light, warm light, rotating strobe, multiple beams, red and white stripes, keeper visible, boat",
}


def main() -> int:
    scenario = json.loads((HERE / "scenario.json").read_text(encoding="utf-8"))
    package = build_paste.build(scenario)

    package["_howto"] = (
        "One shot per generation. Paste the shot's 'paste' value into Kling's main "
        "prompt box and the shot's 'negative' value into Kling's negative prompt box - "
        "they are separate fields and mixing them is what produces the thing you asked "
        "to avoid. Same model version, same mode, same seed for all eight. "
        "Camera movement: none/custom, never auto."
    )
    for shot in package["shots"]:
        shot["negative"] = ", ".join(
            [GLOBAL_NEGATIVE, EXTRA_NEGATIVE.get(shot["id"], "")]
        ).rstrip(", ")

    out = HERE / "KLING_PASTE.json"
    out.write_text(json.dumps(package, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lengths = [len(s["paste"]) for s in package["shots"]]
    print(f"{out}: {len(package['shots'])} shots, prompts {min(lengths)}-{max(lengths)} chars")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
