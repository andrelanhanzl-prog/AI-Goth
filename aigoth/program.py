"""Datový model "programu" videa a jeho načtení z YAML.

Program je jediný zdroj pravdy: obsah, časování i vzhled. Renderer z něj
jen počítá pixely — žádné obsahové rozhodnutí nesmí být zadrátované v kódu.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any

import yaml

AUTO = "auto"

VALID_BACKGROUNDS = {"solid", "gradient", "image"}
VALID_ALIGNS = {"left", "center", "right"}


class ProgramError(ValueError):
    """Chyba v programu — vždy s odkazem na konkrétní scénu."""


@dataclass(frozen=True)
class Theme:
    background: str = "#08080b"
    foreground: str = "#e8e6e3"
    accent: str = "#8b1e2d"
    font: str | None = None
    font_bold: str | None = None
    grain: float = 0.02
    grain_scale: int = 2  # velikost zrna v pixelech; 1 = per-pixel šum
    vignette: float = 0.55
    title_size: float = 0.075  # podíl výšky snímku
    subtitle_size: float = 0.032

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Theme":
        unknown = set(data) - {f.name for f in cls.__dataclass_fields__.values()}
        if unknown:
            raise ProgramError(f"theme: neznámé klíče {sorted(unknown)}")
        return cls(**data)


@dataclass(frozen=True)
class Scene:
    id: str
    duration: float | str = AUTO
    text: str = ""
    subtitle: str = ""
    background: str = "gradient"
    image: str | None = None
    align: str = "center"
    fade: float = 0.8
    accent: str | None = None  # přebije theme.accent jen pro tuhle scénu

    @property
    def is_auto(self) -> bool:
        return self.duration == AUTO

    @classmethod
    def from_dict(cls, data: dict[str, Any], index: int) -> "Scene":
        known = {f.name for f in cls.__dataclass_fields__.values()}
        unknown = set(data) - known
        if unknown:
            raise ProgramError(f"scéna #{index + 1}: neznámé klíče {sorted(unknown)}")

        scene = cls(**{**data, "id": str(data.get("id", f"scene-{index + 1}"))})

        if scene.background not in VALID_BACKGROUNDS:
            raise ProgramError(
                f"scéna '{scene.id}': background '{scene.background}' "
                f"není z {sorted(VALID_BACKGROUNDS)}"
            )
        if scene.background == "image" and not scene.image:
            raise ProgramError(f"scéna '{scene.id}': background 'image' vyžaduje klíč 'image'")
        if scene.align not in VALID_ALIGNS:
            raise ProgramError(
                f"scéna '{scene.id}': align '{scene.align}' není z {sorted(VALID_ALIGNS)}"
            )
        if not scene.is_auto:
            try:
                seconds = float(scene.duration)
            except (TypeError, ValueError):
                raise ProgramError(
                    f"scéna '{scene.id}': duration musí být číslo v sekundách nebo '{AUTO}'"
                ) from None
            if seconds <= 0:
                raise ProgramError(f"scéna '{scene.id}': duration musí být kladná")
            scene = replace(scene, duration=seconds)
        if scene.fade < 0:
            raise ProgramError(f"scéna '{scene.id}': fade nesmí být záporný")
        return scene


@dataclass(frozen=True)
class Program:
    title: str = "AI-Goth"
    width: int = 1920
    height: int = 1080
    fps: int = 30
    audio: str | None = None
    theme: Theme = field(default_factory=Theme)
    scenes: tuple[Scene, ...] = ()
    source: Path | None = None

    @property
    def resolution(self) -> tuple[int, int]:
        return self.width, self.height

    def resolve_path(self, path: str | None) -> Path | None:
        """Cesty v programu jsou relativní k YAML souboru, ne ke cwd."""
        if path is None:
            return None
        candidate = Path(path)
        if candidate.is_absolute() or self.source is None:
            return candidate
        return (self.source.parent / candidate).resolve()


def load_program(path: str | Path) -> Program:
    path = Path(path)
    if not path.exists():
        raise ProgramError(f"program neexistuje: {path}")

    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ProgramError(f"{path}: kořen programu musí být mapa klíčů")

    known = {"title", "resolution", "fps", "audio", "theme", "scenes"}
    unknown = set(data) - known
    if unknown:
        raise ProgramError(f"{path}: neznámé klíče {sorted(unknown)}")

    resolution = data.get("resolution", [1920, 1080])
    if not (isinstance(resolution, (list, tuple)) and len(resolution) == 2):
        raise ProgramError("resolution musí být dvojice [šířka, výška]")
    width, height = (int(value) for value in resolution)
    if width % 2 or height % 2:
        raise ProgramError("resolution: šířka i výška musí být sudé (požadavek H.264)")

    raw_scenes = data.get("scenes") or []
    if not raw_scenes:
        raise ProgramError(f"{path}: program nemá žádné scény")

    scenes = tuple(Scene.from_dict(dict(item), i) for i, item in enumerate(raw_scenes))
    ids = [scene.id for scene in scenes]
    duplicates = sorted({sid for sid in ids if ids.count(sid) > 1})
    if duplicates:
        raise ProgramError(f"duplicitní id scén: {duplicates}")

    return Program(
        title=str(data.get("title", "AI-Goth")),
        width=width,
        height=height,
        fps=int(data.get("fps", 30)),
        audio=data.get("audio"),
        theme=Theme.from_dict(dict(data.get("theme") or {})),
        scenes=scenes,
        source=path.resolve(),
    )
