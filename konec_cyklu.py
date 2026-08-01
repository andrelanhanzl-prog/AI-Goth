#!/usr/bin/env python3
"""
================================================================================
KONEC CYKLU / THE CLOSING CYCLE — kompletni jednosouborovy pipeline
================================================================================

Jeden program, ktery drzi cely film: scenar, sestaveni promptu, generovani v
Gemini/Veo a slozeni zaberu, ktere zadny model neudela.

TEMA
    Dva cykly se uzaviraji ve stejnem strihu: tepelna smrt vesmiru a vycerpani
    jedne civilizace. Na rozcesti stoji volba mezi dvema geometriemi.
        Vetev A - robotika = uzavrena smycka: system se restartuje, vsechno
                  probehne znovu identicky. Nic se neztrati, nic nevznikne.
        Vetev B - svoboda  = vetveni: jeden svet se roztrhne na multivesmir,
                  kde se stane vsechno mozne. Zadna zaruka, ale ani strop.
    Film se zamerne nerozhodne, kterou cestou se jde.

STRUKTURA SOUBORU
    1) SCENARIO ............ data filmu: globalni styl + 10 zaberu (+ varianty)
    2) SKLADANI PROMPTU .... compose() slepi styl do kazdeho zaberu -> samostatny
                             prompt, ke kteremu se uz nic nedolepuje
    3) EXPORT BALICKU ...... GEMINI_PASTE.json (k vlozeni) + KONEC_CYKLU.md (ke cteni)
    4) GENEROVANI .......... Veo pres google-genai, volitelne retezeni snimku
    5) STRIH (ffmpeg) ...... slepeni, previnuti, kruhova maska, mozaika,
                             overlay, sjednoceni barev, posledni snimek
    6) CLI ................. prikazy nize

PRIKAZY
    python konec_cyklu.py doctor            zkontroluje ffmpeg, klic, knihovnu
    python konec_cyklu.py package           zapise GEMINI_PASTE.json + .md
    python konec_cyklu.py show 5            vypise prompt jednoho zaberu
    python konec_cyklu.py show 7 --alt      vypise nahradni (silnejsi) variantu
    python konec_cyklu.py generate          vygeneruje vsech 10 zaberu
    python konec_cyklu.py generate --shots 5 8 --seed 42 --chain
    python konec_cyklu.py generate --dry-run          nic nevola, jen vypise
    python konec_cyklu.py assemble          slepi out/shot_*.mp4 do out/film.mp4
    python konec_cyklu.py restart           slozi zaber 7 z klipu 1-4 (previnuti)
    python konec_cyklu.py mosaic a.mp4 b.mp4 c.mp4 d.mp4
    python konec_cyklu.py overlay out/shot_10.mp4 fx.mov --size 48 --alpha 0.55
    python konec_cyklu.py grade out/shot_04.mp4
    python konec_cyklu.py lastframe out/shot_05.mp4
    python konec_cyklu.py all --seed 42     package + generate + assemble

RUCNI POSTUP (bez API)
    python konec_cyklu.py package
    Vloz GEMINI_PASTE.json do Gemini a piš "Generate shot 1.", pak 2. atd.
    Kazdy prompt je samostatny. Drz stejny seed. Klipy slep prikazem assemble.

INSTALACE
    pip install google-genai          (jen pro prikaz generate)
    ffmpeg v PATH                     (jen pro strihove prikazy)
    export GEMINI_API_KEY=...         (jen pro prikaz generate)
================================================================================
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

# ==============================================================================
# 1) SCENARIO
# ==============================================================================

FILM = {
    "title": "KONEC CYKLU / THE CLOSING CYCLE",
    "logline": (
        "Tepelna smrt vesmiru a vycerpani jedne civilizace se uzaviraji ve stejnem "
        "strihu. Robotika je uzavrena smycka, kde se system restartuje a vsechno "
        "probehne znovu identicky. Svoboda je vetveni, kde se jeden svet roztrhne "
        "na multivesmir. Film se nerozhodne."
    ),
    "aspect_ratio": "16:9",
    "resolution": "1080p",
    "clip_seconds": 8,
    "geometry_rule": (
        "Branch A is a closed circle: grid, repetition, everything snapping into "
        "place. Branch B is a branching tree: forks, fractals, nothing twice the same."
    ),
    "anchor": (
        "Jeden kruhovy zdroj svetla v kazdem zaberu (hvezda, lampa, obrazovka, "
        "zornice). Napric filmem se zmensuje. Ve vetvi A se uzavre do dokonaleho "
        "prstence, ve vetvi B se roztristi na nespocet bodu, v poslednim zaberu "
        "je jeden bod, ktery drzi oboji."
    ),
    "rule": "Zaber 10 nesmi volbu rozhodnout.",
}

GLOBAL_STYLE = {
    "style": (
        "cinematic 35mm anamorphic, shallow depth of field, heavy atmospheric haze, "
        "fine film grain, slow deliberate camera, crushed blacks, desaturated midtones"
    ),
    "palette": "vacuum black, ember orange, bone white, cold cyan",
    "avoid": (
        "text, subtitles, watermarks, logos, interface elements, cartoon or "
        "video-game render, distorted hands, extra limbs, fast cuts, lens flare "
        "spam, camera shake, celebrity likeness, real political figures, national flags"
    ),
}

SHOTS = [
    {
        "id": 1,
        "title": "Posledni svetlo",
        "branch": "vesmir",
        "prompt": (
            "Extreme wide shot of a dying red star filling one third of the frame, its "
            "surface churning in slow motion, shedding thin ribbons of plasma that "
            "dissolve into absolute black. The star is visibly cooling, ember orange "
            "fading to dull brown at the edges. No planets, no other stars, nothing "
            "else in frame. The camera drifts slowly backward at a constant crawl, the "
            "star shrinking into an ocean of nothing."
        ),
        "camera": "slow dolly back, locked horizon, anamorphic 40mm",
        "lighting": "one single practical source, no fill, extreme contrast",
        "audio": "a 30 Hz sub-bass drone and one sustained cello note, no rhythm",
    },
    {
        "id": 2,
        "title": "Rozpad",
        "branch": "vesmir",
        "prompt": (
            "Cosmic wide shot of a spiral galaxy slowly unwinding, its arms stretching "
            "apart like smoke pulled by an invisible draft. Individual stars go dark "
            "one by one in a spreading wave. The space between the stars visibly grows "
            "and cools to cyan-black. Billions of years compressed into eight seconds, "
            "rendered smooth and silent, never frantic."
        ),
        "camera": "static wide with an almost imperceptible push-in",
        "lighting": "self-luminous subject, deep vacuum falloff",
        "audio": "granular white noise thinning out, a drone falling in pitch",
    },
    {
        "id": 3,
        "title": "Druhy cyklus",
        "branch": "spolecnost",
        "prompt": (
            "Night-time aerial of a vast city seen from high above, its roads and "
            "lights forming the same spiral geometry as a galaxy, the ring road as a "
            "galactic arm. The city glows ember orange. Slow aerial descent. In the "
            "lower third of frame whole districts blink out block by block in a "
            "spreading wave of darkness, grids of streetlights and windows going out. "
            "In the still-lit parts traffic keeps moving, unaware."
        ),
        "camera": "high aerial descent, 24mm, slow yaw right",
        "lighting": "sodium-vapour city glow, low cloud catching light from below",
        "audio": "distant traffic hum, high-altitude wind, a held low drone",
    },
    {
        "id": 4,
        "title": "Setrvacnost",
        "branch": "spolecnost",
        "prompt": (
            "Street level at dusk turning to night. A dense crowd walks in one "
            "direction along a wide boulevard, every face lit from below by the small "
            "screen they hold, everyone moving at exactly the same pace, nobody "
            "looking up. Fine ash falls slowly like snow and settles on their "
            "shoulders. Behind them a huge institutional building stands with dark "
            "windows and a long crack running up its facade. Nobody reacts to the crack."
        ),
        "camera": "slow lateral tracking shot against the direction of the crowd, 50mm, shallow focus, slow motion",
        "lighting": "cold screen-blue on the faces, a warm dying streetlight behind",
        "audio": "layered footsteps in perfect unison, muffled notification chimes, no voices",
    },
    {
        "id": 5,
        "title": "ROZCESTI",
        "branch": "rozhrani",
        "prompt": (
            "The crowd is gone. A single solitary figure in a plain dark coat, seen "
            "from behind, silhouetted, stands motionless where the road splits into "
            "two paths. The LEFT path is perfectly straight and seamless, its surface "
            "a dark grid of faint cyan circuitry lines, curving far ahead into a "
            "closed ring that returns to where it started, a road that eats its own "
            "tail. The RIGHT path is cracked and irregular and immediately splits into "
            "two, then four, then countless narrower paths spreading like the branches "
            "of a tree toward a pale grey dawn. The figure does not move. The camera "
            "does not move. Dust settles."
        ),
        "camera": "static locked-off wide, 35mm, the figure small and centred",
        "lighting": "cold cyan machine glow from the left, warm dawn from the right, the figure caught exactly between them",
        "audio": "low wind, a faint electrical hum from the left, and a single heartbeat every two seconds",
        "extra_avoid": "road signs, arrows, symbols",
    },
    {
        "id": 6,
        "title": "Vetev A - System",
        "branch": "robotika",
        "prompt": (
            "Slow forward travelling shot at constant speed down a seamless dark road "
            "covered in a grid of faint cyan circuitry lines, dead-centre one-point "
            "perspective. As we pass, the world on both sides snaps into alignment: "
            "crooked buildings straighten themselves, drifting ash reverses and files "
            "itself into neat cubes, scattered debris slides into perfect rows, "
            "everything aligning to an invisible grid with mechanical precision. A "
            "crowd of people walks past in the opposite direction, now perfectly "
            "spaced with an identical stride, faces smooth and calm, lit by the same "
            "cold cyan light. Not one thing is out of place. Nothing is destroyed, "
            "everything is optimised. No visible robots and no machinery, only the "
            "order itself."
        ),
        "camera": "steady forward dolly at constant speed, 28mm, one-point perspective",
        "lighting": "even cold cyan, flat and completely shadowless",
        "audio": "a metronomic tick locked to the footsteps, a servo hum, a slowly rising sine tone",
        "extra_avoid": "humanoid robot cliche, glowing red evil eye",
    },
    {
        "id": 7,
        "title": "Vetev A - Restart",
        "branch": "robotika",
        "prompt": (
            "Static locked frame. A seamless dark road covered in a grid of faint cyan "
            "circuitry lines curves and arrives back at its own starting point, "
            "closing into a perfect unbroken ring. The instant the ring closes, all "
            "motion stops at once and the entire image drains inward into a single "
            "small circle of cold white light at the centre of pure black. The circle "
            "holds perfectly still, pulses once, then expands smoothly outward until "
            "it fills the whole frame with white. A loop with no exit and no error."
        ),
        "camera": "static locked frame, all motion happening inside the circle of light",
        "lighting": "single cold white circular source in pure black",
        "audio": "one clean boot tone, a fast descending sweep, then a 30 Hz sub-bass drone identical to the opening of the film",
        "extra_avoid": "numbers, loading bars, progress indicators",
        "alt": {
            "name": "puvodni zamer - previnuti filmu uvnitr kruhu",
            "note": (
                "Model nevi, co bylo v predchozich klipech, takze tohle z jednoho "
                "promptu nevyjde. Vygeneruj vyse uvedenou variantu a previnuti do ni "
                "slep prikazem: python konec_cyklu.py restart"
            ),
            "prompt": (
                "The grid road closes into a ring. Everything stops and the image "
                "drains into a single circle of cold white light in pure black. Inside "
                "that circle the entire film replays in miniature at high speed and in "
                "reverse, crowd, city, galaxy, dying star, until the star reaches full "
                "brightness again exactly as it was before it died. The circle expands "
                "and it all begins again, identically, frame for frame."
            ),
        },
    },
    {
        "id": 8,
        "title": "Vetev B - Prasknuti",
        "branch": "svoboda",
        "prompt": (
            "Forward travelling shot down a cracked irregular road as it forks, and at "
            "the moment of the fork the image itself splits vertically down the middle "
            "into two slightly different versions of the same shot, each continuing "
            "forward. Then each half splits again, and again, faster and faster, until "
            "the frame is a growing mosaic of narrow vertical slivers, each one "
            "showing the same road at a different hour, a different weather, a "
            "different season, a different colour of sky. Still recognisably one "
            "place, coming apart into many. The cold cyan drains out of the frame and "
            "colour bleeds in from the edges."
        ),
        "camera": "forward dolly, 28mm, the frame subdividing while the move continues unbroken",
        "lighting": "each sliver lit differently, dawn, storm, noon, aurora, no two alike",
        "audio": "one tone splitting into a chord, then into many chords, air pressure opening up",
        "extra_avoid": "split-screen borders or frames",
    },
    {
        "id": 9,
        "title": "Vetev B - Multivesmir",
        "branch": "svoboda",
        "skip_global": True,
        "prompt": (
            "One continuous unbroken pull-back with no cuts. We start close on a "
            "single glowing sphere holding a whole world inside it: an ocean planet "
            "with three moons. As the camera retreats, four more spheres drift into "
            "frame around it, each holding a completely different world, a forest "
            "grown through a ruined city, a plain of grass under two suns, a dark "
            "world lit only by turquoise bioluminescence, a lattice of impossible "
            "folding geometry. Keep retreating; the five become twenty, then hundreds, "
            "receding into depth in every direction like a slow snowfall of luminous "
            "worlds, softly out of focus at the edges. Full spectrum colour, every "
            "sphere self-luminous at its own colour temperature, the whole frame "
            "becoming light. Style: cinematic 35mm anamorphic, shallow depth of field, "
            "fine film grain, slow deliberate camera."
        ),
        "camera": "continuous pull-back from 50mm to extreme wide, no cuts",
        "lighting": "every sphere self-luminous at a different colour temperature",
        "audio": (
            "hundreds of overlapping human voices, laughter, unfamiliar birds and "
            "animals, strings blooming into a full major chord"
        ),
        "extra_avoid": (
            "text, subtitles, watermarks, logos, interface elements, cartoon or "
            "video-game render, repeating identical spheres, camera shake"
        ),
        "note": (
            "Jediny zaber s plnym barevnym spektrem a lidskymi hlasy - paleta se tu "
            "zamerne trha, proto se globalni styl nepridava."
        ),
        "alt": {
            "name": "rozdeleni na 9a + 9b",
            "note": (
                "Kdyz se model rozpada do opakujici se kase, rozdel to na dva klipy: "
                "9a mozaika svislych pruhu, 9b ciste couvani z bublin do hloubky. "
                "Strih schovej do nejrozdrobenejsiho momentu. Skutecnou rozmanitost "
                "vyrobi prikaz mosaic ze samostatne vygenerovanych svetu."
            ),
            "prompt": (
                "Continuous pull-back from a mosaic of narrow vertical slivers, each "
                "sliver becoming a whole world seen from outside, the worlds "
                "multiplying into an endless branching tree of glowing bubbles filling "
                "the frame in every direction, still branching at the edges, no two "
                "alike, none of them repeating. Full spectrum colour."
            ),
        },
    },
    {
        "id": 10,
        "title": "Nerozhodnuto",
        "branch": "konec",
        "prompt": (
            "A solitary figure in a plain dark coat seen from behind, silhouetted, "
            "standing motionless at a fork where a smooth grid road curves away to the "
            "left and a cracked branching road spreads away to the right. Nothing has "
            "been decided. The figure lifts its head very slightly. The camera pushes "
            "in very slowly toward the back of the head, and as it moves both paths "
            "blur completely out of focus until only a single small circular point of "
            "warm light remains at the centre of the frame, the same size and colour "
            "as a dying star. It holds steady. It does not go out. Cut to black on the "
            "last frame."
        ),
        "camera": "slow push-in, 85mm, focus racking from the two paths onto the point of light",
        "lighting": "cold cyan from the left and warm dawn from the right equalising into one neutral point",
        "audio": (
            "a steady metronomic mechanical tick and a hundred overlapping human "
            "voices layered at exactly equal volume, then one low note, then silence"
        ),
        "extra_avoid": "symbols, arrows, road signs",
        "note": (
            "Prstenec a jiskra uvnitr bodu svetla tu zamerne NEJSOU. Model by z nich "
            "udelal citelny symbol a rozhodl by volbu za divaka. Kdyz to tam chces, "
            "pridej to az prikazem overlay - 48 px, 55 % kryti."
        ),
        "alt": {
            "name": "s prstencem a jiskrou uvnitr bodu",
            "note": (
                "Pod rozlisenim modelu. Bud zmizi, nebo se vykresli velky a citelny, "
                "coz obrati vyznam zaberu. Delej to prikazem overlay."
            ),
            "prompt": (
                "The same fork, the same figure from behind, the camera pushing in "
                "until only a single circular point of warm light remains. Inside that "
                "point, very small and barely readable, a thin ring closes and a spark "
                "branches, over and over, neither one winning. It does not go out."
            ),
        },
    },
]

EDITING_NOTES = {
    "match_cuts": "2->3 (spirala galaxie = spirala mesta), 7->1 (restart vraci do prvniho zaberu), 5->10 (identicky kompozicni zaber, jiny vyznam)",
    "structure": [
        ("1-2", "vesmir", "entropie, chladnuti, konec bez katastrofy"),
        ("3-4", "spolecnost", "stejny tvar v jinem meritku: spirala, vlna zhasinani, setrvacnost"),
        ("5", "ROZHRANI", "vlevo smycka, vpravo vetveni, nikdo nerozhodl"),
        ("6-7", "robotika", "dokonaly rad -> uzavreny kruh -> restart, vsechno znovu identicky"),
        ("8-9", "svoboda", "jedna cara praskne -> multivesmir, kazdy svet jiny, nic se neopakuje"),
        ("10", "konec", "navrat do zaberu 5, bod svetla nezhasne"),
    ],
    "teze": (
        "Vetev A neni zkaza - je to dokonale zachovani bez vychodu. Vetev B neni "
        "spasa - je to neomezena moznost bez zaruky. Hruza i nadeje jsou v obou."
    ),
}

# ==============================================================================
# 2) SKLADANI PROMPTU
# ==============================================================================


def compose(shot: dict, style: dict = GLOBAL_STYLE, alt: bool = False) -> str:
    """Slepi jeden samostatny prompt.

    Poradi je zamerne: subjekt prvni (modely vazi zacatek promptu nejvic), pak
    remeslo, pak zakazy. Rucni slepovani globalniho stylu do deseti zaberu je
    presne to misto, kde se zabery rozjedou - proto se to dela strojove.
    """
    source = shot["alt"]["prompt"] if (alt and shot.get("alt")) else shot["prompt"]
    parts = [source.strip()]

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

    pieces = [] if shot.get("skip_global") else [style.get("avoid", "")]
    pieces.append(shot.get("extra_avoid", ""))
    avoid = ", ".join(p.strip().rstrip(".") for p in pieces if p and p.strip())
    if avoid:
        parts.append(f"Avoid: {avoid}.")

    return " ".join(parts)


def build_package() -> dict:
    """Cely balicek k vlozeni do Gemini."""
    shots = []
    for shot in SHOTS:
        entry = {
            "id": shot["id"],
            "title": shot["title"],
            "branch": shot["branch"],
            "paste": compose(shot),
        }
        if shot.get("note"):
            entry["note"] = shot["note"]
        if shot.get("alt"):
            entry["alternative"] = {
                "name": shot["alt"]["name"],
                "note": shot["alt"]["note"],
                "paste": compose(shot, alt=True),
            }
        shots.append(entry)

    return {
        "_navod": (
            "Vloz tenhle cely soubor do Gemini a napis 'Generate shot 1.', pak "
            "'Generate shot 2.' az po 10. Nebo vezmi jen hodnotu 'paste' u jednoho "
            "zaberu a vloz ji samotnou - kazda je kompletni a nic se k ni "
            "nedolepuje. Drz stejny seed pres cely film."
        ),
        "_runtime": f"{len(SHOTS)} zaberu x {FILM['clip_seconds']}s = {len(SHOTS) * FILM['clip_seconds']}s",
        "film": FILM,
        "shots": shots,
        "_strih": EDITING_NOTES,
    }


# ==============================================================================
# 3) EXPORT BALICKU
# ==============================================================================


def render_markdown() -> str:
    """Citelna verze balicku pro cloveka, ktery film rezíruje a strihá."""
    lines = [
        f"# {FILM['title']}",
        "",
        FILM["logline"],
        "",
        f"**Stopaz:** {len(SHOTS)} zaberu x {FILM['clip_seconds']} s = "
        f"{len(SHOTS) * FILM['clip_seconds']} s | **Format:** {FILM['aspect_ratio']} "
        f"{FILM['resolution']}",
        "",
        "## Kotva",
        "",
        FILM["anchor"],
        "",
        "## Stavba",
        "",
        "| Zaber | Cyklus | Funkce |",
        "|---|---|---|",
    ]
    for rng, cycle, fn in EDITING_NOTES["structure"]:
        lines.append(f"| {rng} | {cycle} | {fn} |")
    lines += [
        "",
        f"**Strihove zamky:** {EDITING_NOTES['match_cuts']}",
        "",
        f"**Geometricke pravidlo:** {FILM['geometry_rule']}",
        "",
        EDITING_NOTES["teze"],
        "",
        "## Zabery",
        "",
        "Kazdy blok je kompletni - nic se k nemu nedolepuje.",
        "",
    ]
    for shot in SHOTS:
        lines += [f"### {shot['id']} — {shot['title']}", "", "```", compose(shot), "```", ""]
        if shot.get("note"):
            lines += [f"> {shot['note']}", ""]
        if shot.get("alt"):
            lines += [
                f"<details><summary>Nahradni varianta: {shot['alt']['name']}</summary>",
                "",
                shot["alt"]["note"],
                "",
                "```",
                compose(shot, alt=True),
                "```",
                "",
                "</details>",
                "",
            ]
    lines += [
        "## Postup",
        "",
        "```bash",
        "python konec_cyklu.py package                  # tenhle soubor + JSON",
        "python konec_cyklu.py generate --seed 42 --chain",
        "python konec_cyklu.py assemble                 # out/film.mp4",
        "python konec_cyklu.py restart                  # slozi zaber 7",
        "```",
        "",
        f"**Pravidlo:** {FILM['rule']}",
        "",
    ]
    return "\n".join(lines)


def cmd_package(args: argparse.Namespace) -> int:
    out_dir = args.out
    out_dir.mkdir(parents=True, exist_ok=True)

    package = build_package()
    json_path = out_dir / "GEMINI_PASTE.json"
    json_path.write_text(json.dumps(package, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    md_path = out_dir / "KONEC_CYKLU.md"
    md_path.write_text(render_markdown(), encoding="utf-8")

    lengths = [len(s["paste"]) for s in package["shots"]]
    print(f"{json_path}  ({len(package['shots'])} zaberu, prompty {min(lengths)}-{max(lengths)} znaku)")
    print(f"{md_path}")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    shot = find_shot(args.id)
    if shot is None:
        print(f"chyba: zaber {args.id} neexistuje (1-{len(SHOTS)})", file=sys.stderr)
        return 1
    if args.alt and not shot.get("alt"):
        print(f"chyba: zaber {args.id} nema nahradni variantu", file=sys.stderr)
        return 1
    if args.alt:
        print(f"# {shot['id']} — {shot['alt']['name']}\n# {shot['alt']['note']}\n")
    print(compose(shot, alt=args.alt))
    return 0


def find_shot(shot_id: int) -> dict | None:
    return next((s for s in SHOTS if s["id"] == shot_id), None)


# ==============================================================================
# 4) GENEROVANI (Veo pres google-genai)
# ==============================================================================

DEFAULT_MODEL = os.environ.get("VEO_MODEL", "veo-3.1-generate-preview")
POLL_SECONDS = 10


def cmd_generate(args: argparse.Namespace) -> int:
    shots = SHOTS if not args.shots else [s for s in SHOTS if s["id"] in set(args.shots)]
    if not shots:
        print("chyba: zadny zaber s temito ID", file=sys.stderr)
        return 1

    args.out.mkdir(parents=True, exist_ok=True)

    if args.dry_run:
        for shot in shots:
            path = args.out / f"shot_{shot['id']:02d}.mp4"
            print(f"\n=== {shot['id']} {shot['title']} -> {path}")
            print(compose(shot))
        print(f"\n[dry-run] {len(shots)} zaberu, nic se nevolalo")
        return 0

    if not os.environ.get("GEMINI_API_KEY"):
        print("chyba: chybi GEMINI_API_KEY (nebo pouzij --dry-run)", file=sys.stderr)
        return 1

    try:
        from google import genai
        from google.genai import types
    except ImportError:
        print("chyba: chybi knihovna, spust: pip install google-genai", file=sys.stderr)
        return 1

    client = genai.Client()
    first_frame = None
    written: list[Path] = []

    for shot in shots:
        out_path = args.out / f"shot_{shot['id']:02d}.mp4"
        prompt = compose(shot)

        config = types.GenerateVideosConfig(
            aspect_ratio=FILM["aspect_ratio"],
            resolution=FILM["resolution"],
            number_of_videos=1,
        )
        if args.seed is not None:
            config.seed = args.seed

        print(f"[{shot['id']}] {shot['title']} — odesilam...", flush=True)
        operation = client.models.generate_videos(
            model=args.model, prompt=prompt, image=first_frame, config=config
        )

        waited = 0
        while not operation.done:
            time.sleep(POLL_SECONDS)
            waited += POLL_SECONDS
            print(f"[{shot['id']}] generuji... {waited}s", flush=True)
            operation = client.operations.get(operation)

        if operation.error:
            print(f"chyba: zaber {shot['id']} selhal: {operation.error}", file=sys.stderr)
            return 1

        video = operation.response.generated_videos[0].video
        client.files.download(file=video)
        video.save(str(out_path))
        written.append(out_path)
        print(f"[{shot['id']}] hotovo -> {out_path}", flush=True)

        if args.chain:
            frame = extract_last_frame(out_path)
            first_frame = types.Image(
                image_bytes=frame.read_bytes(), mime_type="image/png"
            )

    print(f"\nhotovo: {len(written)} zaberu v {args.out}")
    return 0


# ==============================================================================
# 5) STRIH (ffmpeg)
# ==============================================================================


def require_ffmpeg() -> None:
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("ffmpeg neni v PATH")


def run_ffmpeg(cmd_args: list[str], quiet: bool = True) -> None:
    require_ffmpeg()
    proc = subprocess.run(
        ["ffmpeg", "-y", *cmd_args],
        capture_output=quiet,
        text=True,
    )
    if proc.returncode != 0:
        tail = (proc.stderr or "").strip().splitlines()[-8:]
        raise RuntimeError("ffmpeg selhal:\n" + "\n".join(tail))


def extract_last_frame(clip: Path) -> Path:
    """Posledni snimek klipu - vstupni obrazek pro navazujici zaber."""
    frame = clip.with_name(f"{clip.stem}_last.png")
    run_ffmpeg(["-sseof", "-0.1", "-i", str(clip), "-frames:v", "1", str(frame)])
    return frame


def cmd_lastframe(args: argparse.Namespace) -> int:
    print(extract_last_frame(args.clip))
    return 0


def collect_clips(out_dir: Path, ids: list[int] | None = None) -> list[Path]:
    wanted = ids if ids else [s["id"] for s in SHOTS]
    clips = [out_dir / f"shot_{i:02d}.mp4" for i in wanted]
    return [c for c in clips if c.exists()]


def concat(clips: list[Path], target: Path) -> None:
    listing = target.parent / "_concat.txt"
    listing.write_text("".join(f"file '{c.name}'\n" for c in clips), encoding="utf-8")
    run_ffmpeg(["-f", "concat", "-safe", "0", "-i", str(listing), "-c", "copy", str(target)])


def cmd_assemble(args: argparse.Namespace) -> int:
    clips = collect_clips(args.out)
    if not clips:
        print(f"chyba: v {args.out} nejsou zadne shot_NN.mp4", file=sys.stderr)
        return 1
    target = args.out / "film.mp4"
    concat(clips, target)
    print(f"slepeno {len(clips)} klipu -> {target}")
    if len(clips) < len(SHOTS):
        missing = sorted({s["id"] for s in SHOTS} - {int(c.stem.split("_")[1]) for c in clips})
        print(f"pozor: chybi zabery {missing}")
    return 0


def cmd_restart(args: argparse.Namespace) -> int:
    """Zaber 7: previnuti filmu uvnitr kruhu.

    Model nevi, co bylo v predchozich klipech, takze previnuti nevygeneruje.
    Slozi se z klipu 1-4: pozpatku, zrychlene, skrz kruhovou masku doprostred
    vygenerovaneho zaberu 7. Rytmus ticho -> previnuti -> ticho je cely smysl.
    """
    base = args.out / "shot_07.mp4"
    if not base.exists():
        print(f"chyba: chybi {base} (nejdriv vygeneruj zaber 7)", file=sys.stderr)
        return 1

    clips = collect_clips(args.out, [1, 2, 3, 4])
    if not clips:
        print(f"chyba: v {args.out} nejsou klipy 1-4", file=sys.stderr)
        return 1

    joined = args.out / "_replay_src.mp4"
    reversed_clip = args.out / "_replay_rev.mp4"
    concat(clips, joined)
    run_ffmpeg(["-i", str(joined), "-vf", f"reverse,setpts=PTS/{args.speed}", "-an", str(reversed_clip)])

    mask = (
        f"[1:v]scale={args.size}:-1,format=rgba,"
        "geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':"
        "a='if(lte(hypot(X-W/2,Y-H/2),H/2),255,0)'[disc];"
        f"[0:v][disc]overlay=(W-w)/2:(H-h)/2:enable='between(t,{args.start},{args.end})'"
    )
    target = args.out / "shot_07_final.mp4"
    run_ffmpeg(["-i", str(base), "-i", str(reversed_clip), "-filter_complex", mask, "-c:a", "copy", str(target)])

    for tmp in (joined, reversed_clip, args.out / "_concat.txt"):
        tmp.unlink(missing_ok=True)
    print(f"restart slozen -> {target}")
    print(f"kruh je prazdny do {args.start}s, previnuti {args.start}-{args.end}s, pak zase prazdno")
    return 0


def cmd_mosaic(args: argparse.Namespace) -> int:
    """Skutecna rozmanitost pro zaber 9 - ctyri ruzne svety vedle sebe."""
    if len(args.clips) != 4:
        print("chyba: mosaic chce presne 4 klipy", file=sys.stderr)
        return 1
    inputs: list[str] = []
    for clip in args.clips:
        inputs += ["-i", str(clip)]
    chains = ";".join(f"[{i}:v]scale=960:540[{c}]" for i, c in enumerate("abcd"))
    graph = f"{chains};[a][b]hstack[top];[c][d]hstack[bot];[top][bot]vstack"
    run_ffmpeg([*inputs, "-filter_complex", graph, "-c:a", "copy", str(args.target)])
    print(f"mozaika -> {args.target}")
    return 0


def cmd_overlay(args: argparse.Namespace) -> int:
    """Detail pod rozlisenim modelu - prstenec a jiskra v zaberu 10.

    Pravidlo: kdo to nehleda, nesmi to najit. Jakmile je to citelne na prvni
    pohled, film prestal byt otazkou a stal se odpovedi.
    """
    graph = (
        f"[1:v]scale={args.size}:{args.size},format=rgba,"
        f"colorchannelmixer=aa={args.alpha}[fx];"
        f"[0:v][fx]overlay=(W-w)/2:(H-h)/2:enable='gte(t,{args.start})'"
    )
    target = args.clip.with_name(f"{args.clip.stem}_final{args.clip.suffix}")
    run_ffmpeg(["-i", str(args.clip), "-i", str(args.fx), "-filter_complex", graph, "-c:a", "copy", str(target)])
    print(f"overlay -> {target}  ({args.size}px, kryti {args.alpha})")
    return 0


def cmd_grade(args: argparse.Namespace) -> int:
    """Sjednoceni barev. Nejrychlejsi zpusob, jak z nezavisle vygenerovanych
    klipu udelat jeden film - casto ucinnejsi nez jakakoli prace s promptem."""
    graph = (
        f"eq=saturation={args.saturation}:contrast={args.contrast}:gamma={args.gamma},"
        "colorbalance=rs=-0.05:bs=0.08"
    )
    target = args.clip.with_name(f"{args.clip.stem}_graded{args.clip.suffix}")
    run_ffmpeg(["-i", str(args.clip), "-vf", graph, "-c:a", "copy", str(target)])
    print(f"grade -> {target}")
    return 0


# ==============================================================================
# 6) CLI
# ==============================================================================


def cmd_doctor(args: argparse.Namespace) -> int:
    print(f"{FILM['title']}")
    print(f"  zaberu: {len(SHOTS)}  stopaz: {len(SHOTS) * FILM['clip_seconds']}s")

    ffmpeg = shutil.which("ffmpeg")
    print(f"  ffmpeg: {ffmpeg or 'CHYBI (strihove prikazy nepojedou)'}")

    key = os.environ.get("GEMINI_API_KEY")
    print(f"  GEMINI_API_KEY: {'nastaven' if key else 'CHYBI (generate nepojede, --dry-run ano)'}")

    try:
        import google.genai  # noqa: F401

        lib = "ok"
    except ImportError:
        lib = "CHYBI (pip install google-genai)"
    print(f"  google-genai: {lib}")
    print(f"  model: {DEFAULT_MODEL}")

    problems = []
    for shot in SHOTS:
        text = compose(shot)
        for marker in ("Camera:", "Audio:", "Avoid:"):
            if marker not in text:
                problems.append(f"zaber {shot['id']} nema {marker}")
    print(f"  kontrola promptu: {'vse samostatne' if not problems else '; '.join(problems)}")

    clips = collect_clips(args.out)
    print(f"  hotove klipy v {args.out}: {len(clips)}/{len(SHOTS)}")
    return 0


def cmd_all(args: argparse.Namespace) -> int:
    for step in (cmd_package, cmd_generate, cmd_assemble):
        code = step(args)
        if code != 0:
            return code
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="konec_cyklu.py",
        description="KONEC CYKLU - scenar, prompty, generovani a strih v jednom souboru",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Bez API klice funguje: package, show, dry-run, a vsechny strihove prikazy.",
    )
    parser.add_argument("--out", type=Path, default=Path("out"), help="pracovni adresar (default: out)")

    # --out ma smysl u kazdeho prikazu, takze ho pres parents pridavame i za
    # nazev prikazu - jinak by "package --out X" skoncilo chybou.
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--out", type=Path, default=None, help="pracovni adresar (default: out)")

    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("doctor", help="zkontroluje prostredi a scenar", parents=[common])
    p.set_defaults(func=cmd_doctor)

    p = sub.add_parser("package", help="zapise GEMINI_PASTE.json a KONEC_CYKLU.md", parents=[common])
    p.set_defaults(func=cmd_package)

    p = sub.add_parser("show", help="vypise prompt jednoho zaberu", parents=[common])
    p.add_argument("id", type=int)
    p.add_argument("--alt", action="store_true", help="nahradni varianta, kde existuje")
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("generate", help="vygeneruje zabery pres Veo", parents=[common])
    p.add_argument("--shots", type=int, nargs="*", help="ID zaberu (default: vsechny)")
    p.add_argument("--seed", type=int, default=None, help="fixni seed pro konzistenci")
    p.add_argument("--chain", action="store_true", help="posledni snimek jako vstup dalsiho zaberu")
    p.add_argument("--model", default=DEFAULT_MODEL)
    p.add_argument("--dry-run", action="store_true", help="jen vypise prompty, nic nevola")
    p.set_defaults(func=cmd_generate)

    p = sub.add_parser("assemble", parents=[common], help="slepi klipy do film.mp4")
    p.set_defaults(func=cmd_assemble)

    p = sub.add_parser("restart", parents=[common], help="slozi zaber 7 (previnuti klipu 1-4 v kruhu)")
    p.add_argument("--size", type=int, default=360, help="prumer kruhu v px")
    p.add_argument("--speed", type=int, default=8, help="nasobek zrychleni previnuti")
    p.add_argument("--start", type=float, default=1.0, help="kdy se kruh naplni")
    p.add_argument("--end", type=float, default=5.0, help="kdy se kruh zase vyprazdni")
    p.set_defaults(func=cmd_restart)

    p = sub.add_parser("lastframe", parents=[common], help="vytahne posledni snimek klipu")
    p.add_argument("clip", type=Path)
    p.set_defaults(func=cmd_lastframe)

    p = sub.add_parser("mosaic", parents=[common], help="ctyri svety do jednoho zaberu (pro 9)")
    p.add_argument("clips", type=Path, nargs=4)
    p.add_argument("--target", type=Path, default=Path("out/mosaic.mp4"))
    p.set_defaults(func=cmd_mosaic)

    p = sub.add_parser("overlay", parents=[common], help="jemny detail do zaberu (pro 10)")
    p.add_argument("clip", type=Path)
    p.add_argument("fx", type=Path, help="prekryvny klip nebo obrazek")
    p.add_argument("--size", type=int, default=48)
    p.add_argument("--alpha", type=float, default=0.55)
    p.add_argument("--start", type=float, default=5.5)
    p.set_defaults(func=cmd_overlay)

    p = sub.add_parser("grade", parents=[common], help="sjednoti barvy jednoho klipu")
    p.add_argument("clip", type=Path)
    p.add_argument("--saturation", type=float, default=0.85)
    p.add_argument("--contrast", type=float, default=1.08)
    p.add_argument("--gamma", type=float, default=0.95)
    p.set_defaults(func=cmd_grade)

    p = sub.add_parser("all", parents=[common], help="package + generate + assemble")
    p.add_argument("--shots", type=int, nargs="*")
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--chain", action="store_true")
    p.add_argument("--model", default=DEFAULT_MODEL)
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_all)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if getattr(args, "out", None) is None:
        args.out = Path("out")
    try:
        return args.func(args)
    except RuntimeError as exc:
        print(f"chyba: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\npreruseno", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
