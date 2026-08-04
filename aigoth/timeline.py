"""Převod programu na časovou osu — kdy která scéna začíná a končí."""

from __future__ import annotations

from dataclasses import dataclass

from .program import Program, Scene

DEFAULT_AUTO_SECONDS = 6.0


@dataclass(frozen=True)
class Cue:
    scene: Scene
    start: float
    end: float

    @property
    def duration(self) -> float:
        return self.end - self.start

    def local_time(self, t: float) -> float:
        return t - self.start


@dataclass(frozen=True)
class Timeline:
    cues: tuple[Cue, ...]
    duration: float
    warnings: tuple[str, ...] = ()

    def cue_at(self, t: float) -> Cue:
        """Scéna znějící v čase t. Mimo osu vrací krajní scénu."""
        for cue in self.cues:
            if t < cue.end:
                return cue
        return self.cues[-1]

    def frame_count(self, fps: int) -> int:
        return max(1, int(round(self.duration * fps)))


def build_timeline(program: Program, audio_seconds: float | None = None) -> Timeline:
    """Rozvrhne scény. Scény s `duration: auto` si rovným dílem rozeberou
    čas, který ve stopě zbyde po scénách s pevnou délkou."""
    fixed = [s for s in program.scenes if not s.is_auto]
    auto = [s for s in program.scenes if s.is_auto]
    fixed_total = sum(float(s.duration) for s in fixed)
    warnings: list[str] = []

    if auto:
        if audio_seconds is None:
            auto_each = DEFAULT_AUTO_SECONDS
            warnings.append(
                f"bez zvukové stopy: {len(auto)} scén s 'auto' dostalo "
                f"{DEFAULT_AUTO_SECONDS:g}s"
            )
        else:
            remaining = audio_seconds - fixed_total
            if remaining <= 0:
                auto_each = DEFAULT_AUTO_SECONDS
                warnings.append(
                    f"pevné scény ({fixed_total:.1f}s) přesahují stopu "
                    f"({audio_seconds:.1f}s); 'auto' scény dostaly "
                    f"{DEFAULT_AUTO_SECONDS:g}s"
                )
            else:
                auto_each = remaining / len(auto)
    else:
        auto_each = 0.0
        if audio_seconds is not None and abs(audio_seconds - fixed_total) > 0.5:
            warnings.append(
                f"délka scén ({fixed_total:.1f}s) se liší od stopy "
                f"({audio_seconds:.1f}s) o {abs(audio_seconds - fixed_total):.1f}s"
            )

    cues: list[Cue] = []
    cursor = 0.0
    for scene in program.scenes:
        length = auto_each if scene.is_auto else float(scene.duration)
        cues.append(Cue(scene=scene, start=cursor, end=cursor + length))
        cursor += length

    return Timeline(cues=tuple(cues), duration=cursor, warnings=tuple(warnings))
