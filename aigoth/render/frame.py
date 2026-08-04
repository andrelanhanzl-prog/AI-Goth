"""Kreslení jednoho snímku videa.

Vše, co se v rámci scény nemění (pozadí, vysázený text, vinětace), se počítá
jednou a cachuje; per snímek zbyde jen prolnutí, alfa textu a zrno.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageColor, ImageDraw, ImageFont

from ..program import Program, Scene
from ..timeline import Cue, Timeline

FONT_CANDIDATES = (
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
)
FONT_BOLD_CANDIDATES = (
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
)


def _first_existing(paths: tuple[str, ...]) -> str | None:
    for path in paths:
        if Path(path).exists():
            return path
    return None


def _rgb(color: str) -> np.ndarray:
    return np.array(ImageColor.getrgb(color)[:3], dtype=np.float32)


class FrameRenderer:
    def __init__(self, program: Program, timeline: Timeline) -> None:
        self.program = program
        self.timeline = timeline
        self.theme = program.theme
        self.width, self.height = program.resolution

        self._font_path = program.theme.font or _first_existing(FONT_CANDIDATES)
        self._font_bold_path = (
            program.theme.font_bold or _first_existing(FONT_BOLD_CANDIDATES) or self._font_path
        )
        self._fonts: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}
        self._backgrounds: dict[str, np.ndarray] = {}
        self._text_layers: dict[str, np.ndarray] = {}
        self._vignette = self._build_vignette()

    # --- písma ---------------------------------------------------------

    def _font(self, size_ratio: float, bold: bool = False) -> ImageFont.FreeTypeFont:
        size = max(10, int(round(size_ratio * self.height)))
        path = (self._font_bold_path if bold else self._font_path) or ""
        key = (path, size)
        if key not in self._fonts:
            self._fonts[key] = (
                ImageFont.truetype(path, size) if path else ImageFont.load_default(size)
            )
        return self._fonts[key]

    # --- statické vrstvy ------------------------------------------------

    def _build_vignette(self) -> np.ndarray:
        strength = float(np.clip(self.theme.vignette, 0.0, 1.0))
        if strength <= 0:
            return np.ones((self.height, self.width, 1), dtype=np.float32)
        ys = np.linspace(-1.0, 1.0, self.height, dtype=np.float32)[:, None]
        xs = np.linspace(-1.0, 1.0, self.width, dtype=np.float32)[None, :]
        radius = np.sqrt(xs**2 + ys**2) / np.sqrt(2.0)
        mask = 1.0 - strength * np.clip(radius, 0.0, 1.0) ** 1.8
        return mask[:, :, None].astype(np.float32)

    def _background(self, scene: Scene) -> np.ndarray:
        if scene.id in self._backgrounds:
            return self._backgrounds[scene.id]

        accent = _rgb(scene.accent or self.theme.accent)
        base = _rgb(self.theme.background)

        if scene.background == "image":
            layer = self._image_background(scene)
        elif scene.background == "solid":
            layer = np.tile(base, (self.height, self.width, 1)).astype(np.float32)
        else:
            ys = np.linspace(0.0, 1.0, self.height, dtype=np.float32)[:, None, None]
            layer = base * (1.0 - ys) + base * 0.25 * ys
            layer = np.repeat(layer, self.width, axis=1)

        # Měkká záře v akcentní barvě — kotví pohled na střed sazby.
        ys = np.linspace(-0.42, 0.58, self.height, dtype=np.float32)[:, None]
        xs = np.linspace(-0.5, 0.5, self.width, dtype=np.float32)[None, :]
        glow = np.exp(-((xs**2 + ys**2) / 0.10)).astype(np.float32)[:, :, None]
        layer = layer + accent * glow * 0.30

        layer = np.clip(layer * self._vignette, 0, 255).astype(np.float32)
        self._backgrounds[scene.id] = layer
        return layer

    def _image_background(self, scene: Scene) -> np.ndarray:
        path = self.program.resolve_path(scene.image)
        if path is None or not path.exists():
            raise FileNotFoundError(f"scéna '{scene.id}': obrázek nenalezen: {scene.image}")
        image = Image.open(path).convert("RGB")

        # Zvětšit na pokrytí (cover) a středově oříznout.
        scale = max(self.width / image.width, self.height / image.height)
        resized = image.resize(
            (max(1, int(round(image.width * scale))), max(1, int(round(image.height * scale)))),
            Image.LANCZOS,
        )
        left = (resized.width - self.width) // 2
        top = (resized.height - self.height) // 2
        cropped = resized.crop((left, top, left + self.width, top + self.height))
        return np.asarray(cropped, dtype=np.float32) * 0.55

    # --- sazba textu ----------------------------------------------------

    def _wrap(self, text: str, font: ImageFont.FreeTypeFont, max_width: float) -> list[str]:
        lines: list[str] = []
        for paragraph in text.splitlines():
            if not paragraph.strip():
                lines.append("")
                continue
            current = ""
            for word in paragraph.split():
                candidate = f"{current} {word}".strip()
                if font.getlength(candidate) <= max_width or not current:
                    current = candidate
                else:
                    lines.append(current)
                    current = word
            lines.append(current)
        return lines

    def _text_layer(self, scene: Scene) -> np.ndarray:
        """RGBA vrstva s textem scény; alfa se per snímek jen škáluje."""
        if scene.id in self._text_layers:
            return self._text_layers[scene.id]

        canvas = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)
        margin = int(self.width * 0.11)
        max_width = self.width - 2 * margin

        title_font = self._font(self.theme.title_size, bold=True)
        subtitle_font = self._font(self.theme.subtitle_size)
        title_lines = self._wrap(scene.text, title_font, max_width) if scene.text else []
        subtitle_lines = (
            self._wrap(scene.subtitle, subtitle_font, max_width) if scene.subtitle else []
        )

        title_step = title_font.size * 1.30
        subtitle_step = subtitle_font.size * 1.45
        gap = title_font.size * 0.85 if title_lines and subtitle_lines else 0.0
        block = len(title_lines) * title_step + gap + len(subtitle_lines) * subtitle_step
        y = (self.height - block) / 2

        foreground = ImageColor.getrgb(self.theme.foreground)[:3]
        accent = ImageColor.getrgb(scene.accent or self.theme.accent)[:3]

        def draw_line(text: str, font: ImageFont.FreeTypeFont, top: float, color) -> None:
            if not text:
                return
            width = font.getlength(text)
            if scene.align == "left":
                x = margin
            elif scene.align == "right":
                x = self.width - margin - width
            else:
                x = (self.width - width) / 2
            # Jemný stín drží text čitelný i nad světlejším pozadím.
            draw.text((x + 2, top + 3), text, font=font, fill=(0, 0, 0, 140))
            draw.text((x, top), text, font=font, fill=(*color, 255))

        for line in title_lines:
            draw_line(line, title_font, y, foreground)
            y += title_step
        y += gap
        for line in subtitle_lines:
            draw_line(line, subtitle_font, y, accent)
            y += subtitle_step

        layer = np.asarray(canvas, dtype=np.float32)
        self._text_layers[scene.id] = layer
        return layer

    # --- obálky a zrno --------------------------------------------------

    @staticmethod
    def envelope(cue: Cue, t: float) -> float:
        """Alfa textu: náběh na začátku scény, doběh na konci."""
        fade = max(0.0, float(cue.scene.fade))
        if fade <= 0 or cue.duration <= 0:
            return 1.0
        fade = min(fade, cue.duration / 2)
        local = cue.local_time(t)
        rising = local / fade if fade else 1.0
        falling = (cue.duration - local) / fade if fade else 1.0
        return float(np.clip(min(rising, falling), 0.0, 1.0))

    def _grain(self, frame_index: int) -> np.ndarray:
        """Zrno se generuje v hrubším rastru a roztáhne se.

        Per-pixel bílý šum na 1080p jednak nevypadá jako film, jednak zničí
        kompresi — každý snímek je pro kodér nový. Zrno o pár pixelů drží
        vzhled a bitrate zůstane v řádu jednotek Mbit/s.
        """
        amount = float(self.theme.grain)
        if amount <= 0:
            return np.zeros((1, 1, 1), dtype=np.float32)

        scale = max(1, int(self.theme.grain_scale))
        height = max(1, self.height // scale)
        width = max(1, self.width // scale)
        rng = np.random.default_rng(frame_index)  # deterministické — render je reprodukovatelný
        noise = rng.standard_normal((height, width), dtype=np.float32) * (amount * 255.0 * 0.5)
        if scale > 1:
            noise = np.asarray(
                Image.fromarray(noise, mode="F").resize(
                    (self.width, self.height), Image.BILINEAR
                ),
                dtype=np.float32,
            )
        return noise[:, :, None]

    # --- veřejné API ----------------------------------------------------

    def render_at(self, t: float, frame_index: int | None = None) -> Image.Image:
        cue = self.timeline.cue_at(t)
        index = frame_index if frame_index is not None else int(t * self.program.fps)

        frame = self._background(cue.scene)

        # Prolnutí pozadí s předchozí scénou po dobu náběhu.
        position = self.timeline.cues.index(cue)
        fade = min(max(0.0, float(cue.scene.fade)), cue.duration / 2 if cue.duration else 0.0)
        local = cue.local_time(t)
        if position > 0 and fade > 0 and local < fade:
            previous = self._background(self.timeline.cues[position - 1].scene)
            mix = local / fade
            frame = previous * (1.0 - mix) + frame * mix

        text = self._text_layer(cue.scene)
        alpha = (text[:, :, 3:4] / 255.0) * self.envelope(cue, t)
        frame = frame * (1.0 - alpha) + text[:, :, :3] * alpha

        frame = frame + self._grain(index)
        return Image.fromarray(np.clip(frame, 0, 255).astype(np.uint8), mode="RGB")
