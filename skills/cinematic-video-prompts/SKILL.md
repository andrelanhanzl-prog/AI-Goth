---
name: cinematic-video-prompts
description: Builds multi-shot cinematic prompt packages for AI video generators (Veo, Gemini video, Sora, Runway, Kling, Luma, Pika) — shot breakdown, a visual continuity anchor that survives across clips, self-contained copy-paste prompts per shot, and triage of what the model physically cannot render so it goes to editing instead. Use this whenever someone wants a video, film, clip, music video, ad, trailer, or animated sequence made with an AI video tool, wants a prompt to paste into one, asks how to make several generated clips look like one piece, or asks why their generated shots don't match each other — even if they just describe the video they want and never say the word "prompt".
---

# Cinematic video prompts

AI video models generate short clips — typically 4–10 seconds — with no memory of
anything they generated before. A "video" is therefore never one prompt. It is a
set of independent generations that have to be *made* to look like one piece, plus
an edit. Almost every disappointing AI video comes from ignoring one of those two
facts.

Your job is to hand back a package someone can paste in and shoot, not a paragraph
of vibes.

## The workflow

### 1. Find the spine before writing any prompt

Ask what the piece is *about* in one sentence, and what has to be true at the end
that wasn't true at the start. Everything downstream hangs off this. If the user
gave you a theme rather than a story ("the end of the universe", "our brand feels
alive"), propose the spine yourself and say so plainly — most people recognise the
right one instantly but can't generate it cold.

Keep the user's actual subject. Don't quietly swap their idea for a more
conventional one that's easier to render.

### 2. Break it into shots and give the film a shape

Divide the runtime by the model's clip length (8 s is a safe default; say which
you assumed). Then assign each shot a *job* — establish, escalate, turn, pay off.
A ten-shot film with ten beautiful unrelated images is worse than a six-shot film
that moves.

Two structural devices earn their keep constantly:

- **Match cuts.** End one shot on a shape and open the next on the same shape at a
  different scale or subject. This is the cheapest way to make two independently
  generated clips feel causally linked — the eye accepts the cut as intentional.
- **Rhyming framings.** Repeat one exact composition later in the piece with
  something changed. The audience does the emotional work for free.

### 3. Pick a consistency anchor

This is the part people skip and it's the part that decides whether the result
looks like a film or like a folder of clips. Choose one **concrete visual element
that recurs in every shot and changes state across the piece** — a light source, a
colour that's forbidden until a specific moment, a weather condition, a piece of
wardrobe.

It works because you can't ask the model for continuity, but you *can* describe
the same object again in every prompt. The anchor also gives the edit a clock:
if the anchor is at state 1 in shot one and state 10 in shot ten, the film has
visibly travelled.

State the anchor explicitly in the package so the user can hold onto it when they
regenerate a shot.

### 4. Write each shot as a standalone prompt

The single most common practical failure is a package where the style lives in one
place and the shots live in another, so every generation needs manual assembly and
one shot silently drifts. Each shot's prompt must carry everything it needs:

| Element | Why it's there |
|---|---|
| Subject and action | What happens, in present tense, one clear event per shot |
| Camera | Move, lens, angle. "Static locked-off wide" is a real choice, not a missing one |
| Lighting | Source, direction, contrast — this carries mood more than colour does |
| Style | Format, grain, depth of field, grade |
| Palette | Named colours, repeated identically across shots |
| Audio | Ambience, score, and explicitly "no dialogue" if you don't want invented speech |
| Avoid list | Failure modes, not a wish list — see below |

Write in plain declarative English even when talking to the user in another
language; these models are trained overwhelmingly on English caption data and
degrade noticeably otherwise. Say so once rather than silently switching.

Keep one event per shot. Prompts that ask for "she turns, then walks away, then the
door closes" produce mush — the model has 8 seconds and no dramaturgy.

**Avoid lists** should name what actually goes wrong: `text, subtitles, watermarks,
logos, interface elements, distorted hands, extra limbs, fast cuts, camera shake`.
Add the ones specific to your subject — a machine-themed piece wants
`humanoid robot cliché, glowing red evil eye`; a crowd scene wants
`celebrity likeness, real political figures`. Listing things that were never going
to appear just spends attention.

### 5. Triage what the model cannot do

Read back your own shot list and find the ones that ask for something outside a
single generation. This is judgement, not a checklist, but the recurring cases:

- **Anything requiring knowledge of another clip** — a replay, a reversal, a
  callback to an earlier image. The model has never seen the other clip.
- **Unbounded variety** — "a thousand different worlds, no two alike" collapses into
  visible repetition. Name five specific ones and blur the edges; the viewer
  extrapolates the rest.
- **Detail below the resolution the model holds** — a tiny symbol inside a point of
  light either vanishes or, worse, gets rendered large and legible, which can
  invert the meaning of the shot.
- **Exact repetition** — a character or location that must be pixel-identical
  across shots. Use image-to-video from a fixed reference frame instead.
- **Legible text, precise counts, working hands on tools.** Still unreliable.

For each one, give the user two routes: a **simplified prompt** that generates
cleanly, and a **compositing route** that gets the original intent using the clips
they already have. See `references/compositing.md` for ffmpeg recipes covering
reverse-replay, circular masks, mosaics and overlays.

Be honest here rather than optimistic. A user who finds out at generation time
costs themselves a day; a user who is told upfront makes a real choice.

### 6. Ship the package

Produce two files:

- **`GEMINI_PASTE.json`** (or `<tool>_PASTE.json`) — the working document. Metadata
  about the film, then one entry per shot with a single `paste` string containing
  the complete prompt. `scripts/build_paste.py` assembles these from a scenario
  file so the style block is merged in mechanically rather than by hand — use it,
  because hand-merging is exactly where shots drift apart.
- **A readable `.md`** — the same prompts laid out per shot with the structure
  explained, so the user can direct, cut and regenerate rather than just paste.

Tell the user how to run it: paste the JSON, then ask for one shot at a time; hold
the seed fixed across the piece; feed the last frame of a clip in as the first
frame of the next where continuity matters most.

## Craft notes

**Specify camera, don't imply it.** "Cinematic" is not a camera instruction. "Slow
dolly back, 40mm, locked horizon" is.

**Slow beats fast.** Fast motion is where these models fall apart — limbs
duplicate, faces melt. Slow deliberate moves also read as more expensive.

**Lighting sells the shot.** Name the source and let something fall into shadow.
Flat even lighting is the house style of the uncanny.

**Don't resolve what the piece is asking.** If the work poses a question — a
choice, a tension — resist making the final shot explain it. Ambiguity is usually
what the user actually wanted when they came with a theme rather than a plot,
and it's the first thing an eager assistant destroys.

**Structure earns the meaning.** When a piece has two ideas, give them opposed
visual grammars — one built on circles and grids, the other on branches and
fractures — and hold that grammar in every shot of each. The audience reads the
argument without a word of narration.

## References

- `references/shot_grammar.md` — camera moves, lens choices, lighting setups and
  transitions phrased the way video models actually respond to. Read when writing
  the individual shot prompts.
- `references/compositing.md` — ffmpeg recipes for the shots that can't be
  generated: reverse replay, masks, mosaics, overlays, concatenation. Read during
  triage in step 5.
- `scripts/build_paste.py` — merges a scenario JSON into self-contained paste
  strings. `python build_paste.py scenario.json -o GEMINI_PASTE.json`.
