from pathlib import Path

import numpy as np

from aigoth.cli import main
from aigoth.program import Program, Scene, Theme
from aigoth.render.frame import FrameRenderer
from aigoth.render.video import build_command
from aigoth.timeline import build_timeline

PROGRAM = """
title: Test
resolution: [160, 90]
fps: 12
scenes:
  - id: a
    duration: 1
    text: "Zkouška ěščřžýáíé"
    subtitle: "podtitul"
  - id: b
    duration: 1
    text: "druhá"
    background: solid
"""


def small(**kwargs) -> Program:
    return Program(
        width=160,
        height=90,
        fps=12,
        theme=Theme(**kwargs.pop("theme", {})),
        scenes=kwargs.pop("scenes", (Scene("a", 1, text="ahoj"),)),
    )


def test_snimek_ma_spravny_rozmer_a_rezim():
    program = small()
    renderer = FrameRenderer(program, build_timeline(program))
    frame = renderer.render_at(0.5)
    assert frame.size == (160, 90)
    assert frame.mode == "RGB"


def test_render_je_deterministicky():
    program = small()
    timeline = build_timeline(program)
    first = np.asarray(FrameRenderer(program, timeline).render_at(0.5, frame_index=6))
    second = np.asarray(FrameRenderer(program, timeline).render_at(0.5, frame_index=6))
    assert np.array_equal(first, second)


def test_zrno_meni_snimky_v_case():
    program = small(theme={"grain": 0.2})
    timeline = build_timeline(program)
    renderer = FrameRenderer(program, timeline)
    a = np.asarray(renderer.render_at(0.4, frame_index=5), dtype=int)
    b = np.asarray(renderer.render_at(0.4, frame_index=6), dtype=int)
    assert not np.array_equal(a, b)


def test_text_se_na_zacatku_fade_neobjevi():
    scene = Scene("a", 2.0, text="ABC", fade=1.0, accent="#000000")
    program = small(scenes=(scene,), theme={"grain": 0.0})
    renderer = FrameRenderer(program, build_timeline(program))
    dark = np.asarray(renderer.render_at(0.0)).mean()
    lit = np.asarray(renderer.render_at(1.0)).mean()
    assert lit > dark


def test_hrube_zrno_je_mekci_nez_per_pixel():
    """Zrno v hrubším rastru musí mít menší rozdíly mezi sousedními pixely —
    to je celý důvod, proč kvůli němu neexploduje bitrate."""
    scenes = (Scene("a", 1.0, text=""),)
    jemne = small(scenes=scenes, theme={"grain": 0.3, "grain_scale": 1, "vignette": 0.0})
    hrube = small(scenes=scenes, theme={"grain": 0.3, "grain_scale": 4, "vignette": 0.0})

    def sousedni_rozdil(program):
        renderer = FrameRenderer(program, build_timeline(program))
        frame = np.asarray(renderer.render_at(0.5, frame_index=3), dtype=float)
        return np.abs(np.diff(frame, axis=1)).mean()

    assert sousedni_rozdil(hrube) < sousedni_rozdil(jemne)


def test_bez_zrna_se_tune_grain_neposila():
    bez = build_command(small(theme={"grain": 0.0}), Path("o.mp4"), None, 20, "medium")
    assert "-tune" not in bez
    se_zrnem = build_command(small(theme={"grain": 0.05}), Path("o.mp4"), None, 20, "medium")
    assert se_zrnem[se_zrnem.index("-tune") + 1] == "grain"


def test_ffmpeg_prikaz_obsahuje_zvuk_jen_kdyz_je():
    program = small()
    bez = build_command(program, Path("out.mp4"), None, 18, "medium")
    assert "-c:a" not in bez
    s_audiem = build_command(program, Path("out.mp4"), Path("a.wav"), 20, "fast")
    assert s_audiem.count("-i") == 2
    assert "-shortest" in s_audiem
    assert "20" in s_audiem


def test_cli_render_vytvori_video(tmp_path, capsys):
    program = tmp_path / "p.yml"
    program.write_text(PROGRAM, encoding="utf-8")
    output = tmp_path / "out.mp4"
    assert main(["render", str(program), "-o", str(output), "--quiet", "--preset", "ultrafast"]) == 0
    assert output.exists() and output.stat().st_size > 0


def test_cli_hlasi_chybu_misto_traceback(tmp_path, capsys):
    assert main(["validate", str(tmp_path / "nic.yml")]) == 1
    assert "chyba:" in capsys.readouterr().err


def test_cli_preview(tmp_path):
    program = tmp_path / "p.yml"
    program.write_text(PROGRAM, encoding="utf-8")
    output = tmp_path / "snimek.png"
    assert main(["preview", str(program), "-o", str(output), "--at", "0.5"]) == 0
    assert output.exists()
