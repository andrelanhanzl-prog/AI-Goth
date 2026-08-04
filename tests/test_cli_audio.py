"""Náhled musí sedět na render — na stejném čase stejná scéna."""

import subprocess

import pytest

from aigoth.cli import _prepare
from aigoth.ffmpeg import ffmpeg_binary
from aigoth.program import ProgramError

PROGRAM = """
resolution: [160, 90]
fps: 12
audio: ton.wav
scenes:
  - id: intro
    duration: 1
    text: intro
  - id: telo
    text: telo
  - id: konec
    duration: 1
    text: konec
"""


@pytest.fixture
def projekt(tmp_path):
    subprocess.run(
        [ffmpeg_binary(), "-y", "-loglevel", "error", "-f", "lavfi",
         "-i", "sine=frequency=220:duration=5", str(tmp_path / "ton.wav")],
        check=True,
    )
    program = tmp_path / "p.yml"
    program.write_text(PROGRAM, encoding="utf-8")
    return program


def test_auto_scena_se_dopocita_ze_stopy(projekt):
    _, timeline, audio = _prepare(str(projekt))
    assert audio is not None
    assert timeline.cues[1].duration == pytest.approx(3.0, abs=0.05)
    assert timeline.duration == pytest.approx(5.0, abs=0.05)


def test_nahled_ma_stejnou_osu_jako_render(projekt):
    _, render_timeline, _ = _prepare(str(projekt))
    _, preview_timeline, _ = _prepare(str(projekt), audio_required=False)
    assert preview_timeline.cue_at(2.0).scene.id == render_timeline.cue_at(2.0).scene.id
    assert preview_timeline.duration == pytest.approx(render_timeline.duration)


def test_chybejici_stopa_je_pro_render_chyba(tmp_path):
    program = tmp_path / "p.yml"
    program.write_text(PROGRAM, encoding="utf-8")
    with pytest.raises(ProgramError, match="nenalezena"):
        _prepare(str(program))


def test_chybejici_stopa_nahled_nezastavi(tmp_path, capsys):
    program = tmp_path / "p.yml"
    program.write_text(PROGRAM, encoding="utf-8")
    _, timeline, audio = _prepare(str(program), audio_required=False)
    assert audio is None
    assert timeline.duration > 0
