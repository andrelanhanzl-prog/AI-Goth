from aigoth.program import Program, Scene
from aigoth.render.frame import FrameRenderer
from aigoth.timeline import DEFAULT_AUTO_SECONDS, build_timeline


def program(*scenes: Scene, fps: int = 25) -> Program:
    return Program(width=320, height=180, fps=fps, scenes=scenes)


def test_pevne_delky_jdou_za_sebou():
    timeline = build_timeline(program(Scene("a", 2), Scene("b", 3)))
    assert [(c.start, c.end) for c in timeline.cues] == [(0.0, 2.0), (2.0, 5.0)]
    assert timeline.duration == 5.0


def test_auto_sceny_deli_zbytek_stopy():
    timeline = build_timeline(program(Scene("a", 4), Scene("b"), Scene("c")), audio_seconds=10.0)
    assert timeline.cues[1].duration == 3.0
    assert timeline.cues[2].duration == 3.0
    assert timeline.duration == 10.0


def test_auto_bez_zvuku_dostane_vychozi_delku():
    timeline = build_timeline(program(Scene("a")))
    assert timeline.cues[0].duration == DEFAULT_AUTO_SECONDS
    assert any("bez zvukové stopy" in w for w in timeline.warnings)


def test_pevne_sceny_presahujici_stopu_varuji():
    timeline = build_timeline(program(Scene("a", 30), Scene("b")), audio_seconds=10.0)
    assert any("přesahují stopu" in w for w in timeline.warnings)


def test_rozjeta_delka_bez_auto_scen_varuje():
    timeline = build_timeline(program(Scene("a", 4)), audio_seconds=30.0)
    assert any("liší od stopy" in w for w in timeline.warnings)
    assert timeline.duration == 4.0


def test_cue_at_vraci_spravnou_scenu():
    timeline = build_timeline(program(Scene("a", 2), Scene("b", 2)))
    assert timeline.cue_at(0.0).scene.id == "a"
    assert timeline.cue_at(1.99).scene.id == "a"
    assert timeline.cue_at(2.0).scene.id == "b"
    assert timeline.cue_at(99.0).scene.id == "b"  # za koncem drží poslední scénu


def test_pocet_snimku():
    assert build_timeline(program(Scene("a", 2))).frame_count(25) == 50


def test_obalka_nabiha_a_dobiha():
    timeline = build_timeline(program(Scene("a", 4, fade=1.0)))
    cue = timeline.cues[0]
    assert FrameRenderer.envelope(cue, 0.0) == 0.0
    assert FrameRenderer.envelope(cue, 1.0) == 1.0
    assert FrameRenderer.envelope(cue, 2.0) == 1.0
    assert FrameRenderer.envelope(cue, 4.0) == 0.0


def test_obalka_se_vejde_i_do_kratke_sceny():
    """Fade delší než scéna se ořízne na půlku, ne aby text nikdy nenaskočil."""
    timeline = build_timeline(program(Scene("a", 1.0, fade=10.0)))
    cue = timeline.cues[0]
    assert FrameRenderer.envelope(cue, 0.5) == 1.0
