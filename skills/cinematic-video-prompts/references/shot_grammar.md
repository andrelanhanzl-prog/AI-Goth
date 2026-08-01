# Shot grammar for video models

Vocabulary that these models respond to reliably, and the phrasings that quietly
fail. Use while writing individual shot prompts.

## Contents

- [Camera moves](#camera-moves)
- [Lenses and framing](#lenses-and-framing)
- [Lighting](#lighting)
- [Motion and timing](#motion-and-timing)
- [Transitions between shots](#transitions-between-shots)
- [Audio](#audio)
- [Palette discipline](#palette-discipline)
- [Phrasings that fail](#phrasings-that-fail)

## Camera moves

Name the move, the speed, and whether the horizon is locked. One move per shot.

| Move | Phrasing that works | Use for |
|---|---|---|
| Static | `static locked-off wide, no camera movement` | Held moments, dread, a decision |
| Push in | `slow push-in, 85mm, focus racking from X to Y` | Interiority, closing on a realisation |
| Pull back | `continuous unbroken pull-back from 50mm to extreme wide, no cuts` | Revelation of scale |
| Dolly forward | `steady forward dolly at walking pace, 28mm, one-point perspective` | Entering a world, inevitability |
| Lateral track | `slow lateral tracking shot moving against the subject, 50mm` | Observation, alienation |
| Aerial descent | `high aerial descent with a gentle yaw right, 24mm` | Establishing, scale |
| Orbit | `slow orbit around the subject, constant radius` | Reverence — use sparingly, degrades fast |

Handheld reads as noise, not energy — the models render it as jitter. If you want
unease, get it from composition and lighting instead.

## Lenses and framing

Lens numbers work as style signals even though nothing optical is happening:
24–28mm for space and grandeur, 35–50mm for neutral human scale, 85–100mm for
compression and intimacy, macro for texture. Pair the number with the framing
(`extreme wide`, `medium`, `close`, `extreme macro`) rather than relying on it alone.

`shallow depth of field` is the single most effective phrase for making output look
photographed rather than rendered.

## Lighting

Always name a source, a direction and a contrast ratio in words. The difference
between amateur and cinematic output is mostly here.

- `single practical source, no fill, extreme contrast` — hard, dramatic
- `soft key from a window camera left, deep shadow on the right` — classical
- `even flat shadowless light` — clinical, institutional, deliberately inhuman
- `lit from below by a screen, cold blue on the face` — contemporary unease
- `backlit silhouette against a bright haze, subject fully black` — anonymity
- `golden hour, low warm key raking across the frame` — nostalgia; overused

Two-source setups carry conflict cheaply: warm from one side, cold from the other,
subject caught between. If a shot is about a choice, light it as one.

## Motion and timing

Eight seconds holds one event. Two if the second is a consequence of the first.

- Good: `she stops walking and looks up`
- Bad: `she stops, looks up, turns around, and the door closes behind her`

Slow motion is reliable and flattering: `slow motion, 60fps feel`. Speed ramps and
time-lapse are unreliable unless the subject is simple (clouds, crowds, light).

## Transitions between shots

The model can't cut, so transitions are built at the seams:

- **Match cut** — end on a shape, open the next shot on the same shape at a
  different scale. Describe the shape identically in both prompts.
- **Match framing** — repeat an earlier composition verbatim later in the piece.
  Copy the framing sentence word for word so the model lands in the same place.
- **Light bridge** — end one shot expanding to white or draining to black, open the
  next from that state. Clean, forgiving, works in any editor.
- **Frame chaining** — export the last frame of clip N and feed it as the first
  frame of clip N+1 (image-to-video). The strongest continuity available; use it
  where a location or character must persist.

## Audio

Most models generate native audio. If you don't ask, you get generic music or, more
annoyingly, invented mumbled dialogue.

Name ambience, then score, then say `no dialogue` explicitly. Describe score by
texture and interval rather than genre: `a 30 Hz sub-bass drone and one sustained
cello note` beats `epic cinematic soundtrack`.

Audio is also the cheapest place to carry meaning the picture must not state
outright — two sounds at equal volume hold a contradiction the image would have to
resolve.

## Palette discipline

Name three to five colours and repeat the identical list in every shot prompt.
Drifting palettes are the most visible sign of clip-by-clip generation.

A palette you break *once*, deliberately, at the moment the piece turns, is worth
more than any camera move. Say in the package that the break is intentional so the
user doesn't "fix" it.

## Phrasings that fail

| Instead of | Write |
|---|---|
| `cinematic`, `epic`, `stunning`, `4K`, `masterpiece` | actual camera, lens, lighting |
| `beautiful woman` | what she is doing, wearing, and how she is lit |
| `in the style of <living director>` | the technique you want from them |
| `high quality` | `35mm film grain, shallow depth of field` |
| `a lot of people` | `a dense crowd walking in one direction` |
| `text reading "THE END"` | nothing — add text in an editor |
| `zoom in fast` | `slow push-in` |
| a list of five things happening | one thing happening |
