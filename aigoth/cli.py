"""Příkazová řádka: aigoth validate | plan | preview | render."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .ffmpeg import FfmpegMissing, audio_duration
from .program import Program, ProgramError, load_program
from .render.frame import FrameRenderer
from .render.video import render_video
from .timeline import Timeline, build_timeline


def _prepare(path: str, audio_required: bool = True) -> tuple[Program, Timeline, Path | None]:
    """Načte program a rozvrhne osu. Zvuk se čte i pro náhled — jinak by
    `preview --at` ukázal jinou scénu, než jaká v renderu na tom čase je."""
    program = load_program(path)
    audio_path = program.resolve_path(program.audio)
    seconds = None
    if audio_path is not None:
        if audio_path.exists():
            seconds = audio_duration(audio_path)
        elif audio_required:
            raise ProgramError(f"zvuková stopa nenalezena: {audio_path}")
        else:
            print(f"  ! zvuková stopa nenalezena: {audio_path}", file=sys.stderr)
            audio_path = None
    return program, build_timeline(program, seconds), audio_path


def _format_time(seconds: float) -> str:
    minutes, rest = divmod(seconds, 60)
    return f"{int(minutes):02d}:{rest:05.2f}"


def _print_warnings(timeline: Timeline) -> None:
    for warning in timeline.warnings:
        print(f"  ! {warning}", file=sys.stderr)


def cmd_validate(args: argparse.Namespace) -> int:
    program, timeline, audio = _prepare(args.program)
    print(f"✓ {program.title} — {len(timeline.cues)} scén, {_format_time(timeline.duration)}")
    print(f"  {program.width}×{program.height} @ {program.fps} fps")
    print(f"  zvuk: {audio if audio else '—'}")
    _print_warnings(timeline)
    return 0


def cmd_plan(args: argparse.Namespace) -> int:
    program, timeline, _ = _prepare(args.program, audio_required=False)
    print(f"{program.title} — {_format_time(timeline.duration)}\n")
    for cue in timeline.cues:
        headline = " ".join(cue.scene.text.split())
        if len(headline) > 58:
            headline = headline[:57] + "…"
        print(
            f"  {_format_time(cue.start)} → {_format_time(cue.end)}"
            f"  [{cue.duration:6.2f}s]  {cue.scene.id:<14} {headline}"
        )
    _print_warnings(timeline)
    return 0


def cmd_preview(args: argparse.Namespace) -> int:
    program, timeline, _ = _prepare(args.program, audio_required=False)
    renderer = FrameRenderer(program, timeline)
    at = args.at if args.at is not None else timeline.duration / 2
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    renderer.render_at(at, frame_index=int(at * program.fps)).save(output)
    print(f"✓ snímek v čase {_format_time(at)} → {output}")
    return 0


def cmd_render(args: argparse.Namespace) -> int:
    program, timeline, audio = _prepare(args.program)
    _print_warnings(timeline)
    total_frames = timeline.frame_count(program.fps)
    print(
        f"Renderuji {program.title}: {total_frames} snímků, "
        f"{_format_time(timeline.duration)}, {program.width}×{program.height}"
    )

    def progress(done: int, total: int) -> None:
        if done % max(1, total // 50) == 0 or done == total:
            percent = 100 * done / total
            print(f"\r  {percent:5.1f}%  ({done}/{total})", end="", file=sys.stderr, flush=True)

    output = render_video(
        program,
        timeline,
        output=args.output,
        audio=audio,
        crf=args.crf,
        preset=args.preset,
        on_progress=None if args.quiet else progress,
    )
    if not args.quiet:
        print(file=sys.stderr)
    print(f"✓ hotovo → {output}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="aigoth",
        description="Renderuje video z textového programu (YAML) a zvukové stopy.",
    )
    parser.add_argument("--version", action="version", version=f"aigoth {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    def add(name: str, help_text: str, handler) -> argparse.ArgumentParser:
        sub = subparsers.add_parser(name, help=help_text)
        sub.add_argument("program", help="cesta k programu (YAML)")
        sub.set_defaults(handler=handler)
        return sub

    add("validate", "zkontroluje program bez renderu", cmd_validate)
    add("plan", "vypíše časovou osu scén", cmd_plan)

    preview = add("preview", "vyrenderuje jeden snímek do PNG", cmd_preview)
    preview.add_argument("-o", "--output", default="preview.png", help="výstupní PNG")
    preview.add_argument("--at", type=float, help="čas v sekundách (výchozí: půlka videa)")

    render = add("render", "vyrenderuje celé video", cmd_render)
    render.add_argument("-o", "--output", default="out.mp4", help="výstupní MP4")
    render.add_argument("--crf", type=int, default=18, help="kvalita H.264, nižší = lepší")
    render.add_argument("--preset", default="medium", help="ffmpeg preset")
    render.add_argument("-q", "--quiet", action="store_true", help="bez ukazatele průběhu")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.handler(args)
    except (ProgramError, FfmpegMissing, FileNotFoundError) as error:
        print(f"chyba: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
