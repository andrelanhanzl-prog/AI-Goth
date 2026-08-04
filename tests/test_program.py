import pytest

from aigoth.program import AUTO, ProgramError, load_program

MINIMAL = """
title: T
scenes:
  - id: a
    duration: 2
    text: ahoj
"""


def write(tmp_path, text, name="program.yml"):
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


def test_nacte_minimalni_program(tmp_path):
    program = load_program(write(tmp_path, MINIMAL))
    assert program.title == "T"
    assert program.resolution == (1920, 1080)
    assert len(program.scenes) == 1
    assert program.scenes[0].text == "ahoj"


def test_scena_bez_delky_je_auto(tmp_path):
    program = load_program(write(tmp_path, "scenes:\n  - id: a\n    text: x\n"))
    assert program.scenes[0].duration == AUTO
    assert program.scenes[0].is_auto


def test_chybejici_scény_ohlasi_chybu(tmp_path):
    with pytest.raises(ProgramError, match="žádné scény"):
        load_program(write(tmp_path, "title: T\n"))


def test_duplicitni_id(tmp_path):
    text = "scenes:\n  - id: a\n    duration: 1\n  - id: a\n    duration: 1\n"
    with pytest.raises(ProgramError, match="duplicitní"):
        load_program(write(tmp_path, text))


def test_neznamy_klic_ve_scene(tmp_path):
    with pytest.raises(ProgramError, match="neznámé klíče"):
        load_program(write(tmp_path, "scenes:\n  - id: a\n    barva: modrá\n"))


def test_zaporna_delka(tmp_path):
    with pytest.raises(ProgramError, match="kladná"):
        load_program(write(tmp_path, "scenes:\n  - id: a\n    duration: -3\n"))


def test_liche_rozliseni(tmp_path):
    text = "resolution: [1921, 1080]\nscenes:\n  - id: a\n    duration: 1\n"
    with pytest.raises(ProgramError, match="sudé"):
        load_program(write(tmp_path, text))


def test_background_image_bez_obrazku(tmp_path):
    text = "scenes:\n  - id: a\n    duration: 1\n    background: image\n"
    with pytest.raises(ProgramError, match="vyžaduje klíč 'image'"):
        load_program(write(tmp_path, text))


def test_cesty_jsou_relativni_k_programu(tmp_path):
    program = load_program(write(tmp_path, MINIMAL + "audio: stopa.wav\n"))
    assert program.resolve_path(program.audio) == (tmp_path / "stopa.wav").resolve()


def test_chybejici_soubor(tmp_path):
    with pytest.raises(ProgramError, match="neexistuje"):
        load_program(tmp_path / "nic.yml")
