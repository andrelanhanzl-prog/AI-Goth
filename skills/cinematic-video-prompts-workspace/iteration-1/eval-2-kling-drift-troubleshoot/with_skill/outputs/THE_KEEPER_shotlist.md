# THE KEEPER — 8-shot horror short for Kling

**Logline.** A lighthouse keeper carrying a hand lamp up a dark tower discovers the
light he tends has been out for weeks, and that nothing on the island has been
waiting for him.

**Spine.** He believes he is keeping the light. He is not, and has not been for a
long time.

**Runtime.** 8 shots × 5 s = 40 s. Run shots 3, 7 and 8 at 10 s if you want room to
breathe (~55 s).

Prompts are in `KLING_PASTE.json`. Everything below explains *why* each one is
built the way it is, so you can regenerate and recut without the package falling
apart.

---

## Why your clips didn't match — the five causes

| Symptom you have | Actual cause | Fix in this package |
|---|---|---|
| Lighthouse changes shape | You described the building differently each time. The model has no memory; every generation invents the tower from your wording. | **Locked strings** — one word-for-word description of the tower, the keeper and the lamp, pasted identically into every shot. |
| Colour jumps between clips | Palette wasn't restated per shot, and there's no shared grade at the end. | Same four-colour palette line in all eight prompts, plus a single grade pass over the finished clips. |
| One came back a cartoon | Nothing in that prompt said *photographed*, and Kling's negative box was empty. A prompt that reads like a story synopsis defaults toward illustration. | Every prompt carries a photographic style block; every shot ships a filled negative prompt. |
| General inconsistency | Seed floating, and probably a model-version or mode switch mid-session. | Same version, same mode, same seed, all eight. |
| Interiors don't feel like the same building | Not solvable by prompting at all. | **Frame chaining** — see below. |

---

## The consistency anchor

**A brass hurricane lamp with a soot-blackened glass chimney, carried in the
keeper's hand. It is the only working light in the film.**

Every shot is lit by it, so the light quality can't drift far. And it runs a clock:

| Shots | Lamp state |
|---|---|
| 1–3 | small steady amber flame |
| 4–5 | low, guttering |
| 6 | bent flat by the wind |
| 7 | nearly out, blue at the base |
| 8 | gone |

The tower's own light is absent for seven shots. That absence *is* the film, so
the anchor is doing story work as well as continuity work. If you regenerate a
shot, keep the lamp's state for that shot — it's the thing telling the audience
time has moved.

**Palette break.** Cold mercury white-green appears once, in shot 8, and is
forbidden everywhere else. That's deliberate. Don't grade it back toward the warm
end when you're matching clips.

---

## Structure

| # | Job | Shot |
|---|---|---|
| 1 | Establish | The tower is dark. One amber flame climbs the stair windows. |
| 2 | Establish | The keeper climbs, carrying the only light in the film. |
| 3 | Escalate | The Fresnel lens is furred with salt. The burner is cold. |
| 4 | Escalate | Logbook: the same entry, page after page after page. |
| 5 | **Turn** | Supply crates outside, unopened, weed-grown. Weeks have passed. |
| 6 | Escalate | A hull passes close in the dark, unwarned. No beam reaches it. |
| 7 | Turn | He strikes a match. In the glass, the stairwell has a shape in it. |
| 8 | Pay off | Opening framing repeated. The light comes on. The lamp is gone. |

**Match cut, 3 → 4.** Shot 3 ends on the dead lens filling the frame as a circle.
Shot 4 opens on a ring of lamp soot on the logbook page — same shape, different
scale. Cut on the circle and the two independently generated clips read as
causally linked.

**Rhyming framing, 3 → 7.** Shot 7 uses shot 3's camera line word for word. Same
room, same move, same lens — and the second time, the light catches. The audience
does the emotional work for free.

**Rhyming framing, 1 → 8.** Same trick at the outer edges of the film. Identical
composition, everything changed.

**Don't resolve it.** Shot 8 shows a working light and no keeper. It does not
explain which of those two things is the horror. Leave it there.

---

## What Kling can't do — triage

Four shots ask for something outside a single generation. Each gets a clean route
and a compositing route.

### Shot 4 — the repeated logbook entry
Legible, consistent handwriting is still unreliable. Asked for it directly, you
get either mush or, worse, large legible nonsense that reads as a mistake.

- **Simplified (in the package):** "unreadable ink strokes only, no legible words
  and no numbers, softening out of focus toward the edges." The *rhythm* of
  identical lines carries the point; nobody needs to read them.
- **Compositing route:** generate the clean plate as written, photograph or set a
  real page of repeated handwriting, and overlay it in the editor with a
  perspective corner-pin. Twenty minutes, and it's the one shot where a legible
  detail is worth having.

### Shot 7 — the figure in the lens
Ask a model for a second figure reflected in curved glass and you get a duplicated
body, a melted face, or the figure standing in the room.

- **Simplified (in the package):** the stairwell reads as "one tall vertical
  absence where the reflections do not appear." A hole in the pattern is more
  frightening than a rendered ghost and it generates reliably.
- **Compositing route:** generate a second 5 s clip of a standing silhouette
  against black, then overlay it into the lens area at very low opacity:

  ```bash
  ffmpeg -y -i out/shot_07.mp4 -i out/figure.mp4 -filter_complex \
  "[1:v]scale=180:-1,format=rgba,colorchannelmixer=aa=0.18[fx]; \
   [0:v][fx]overlay=(W-w)/2:(H-h)/2:enable='between(t,2.5,4)'" \
  -c:a copy out/shot_07_final.mp4
  ```

  If someone who isn't looking for it can spot it, it's too strong.

### Shot 8 — the callback to shot 1
The model has never seen shot 1, so it cannot match its framing on request.

- **Route:** generate shot 8 as **image-to-video from shot 1's first frame**.
  Extract it, feed it as the start frame, and let the prompt only describe the
  change (windows dark, beam on):

  ```bash
  ffmpeg -y -i out/shot_01.mp4 -frames:v 1 out/shot_01_first.png
  ```

  This is the single highest-leverage move in the package. Prompt wording will
  never get you a matching composition; a start frame gets it for free.

### All eight — the lighthouse itself
A location that must be recognisably the same building across eight text-to-video
generations is outside what prompting can hold, no matter how good the wording.

- **Route:** generate shot 1 first, and treat it as your reference. Then
  **frame-chain the seams**: last frame of shot 2 → start frame of shot 3, last
  frame of shot 3 → start frame of shot 4, and so on for the interiors, which are
  where shape drift is most visible.

  ```bash
  ffmpeg -y -sseof -0.1 -i out/shot_02.mp4 -frames:v 1 out/shot_02_last.png
  ```

  If your Kling version has multi-image reference ("Elements"), feed it the same
  two stills — the tower exterior and the keeper — for every shot.

---

## How to run it

1. **Lock your settings before shot 1 and don't touch them.** Same model version,
   same mode (Pro/Master — pick one), same aspect ratio, same seed, same duration.
   Push the relevance / prompt-adherence slider up and creativity down. Set camera
   movement to **none or custom** — Kling's auto camera is a drift source, and
   every shot here already specifies its move in words.
2. **Two boxes, not one.** The `paste` value goes in the main prompt. The
   `negative` value goes in Kling's negative prompt box. Do not paste the negative
   list into the main prompt — naming "cartoon" inside a positive prompt is a
   reliable way to get one.
3. **Generate shot 1, then 2, then 3.** In order. You need shot 1's frames for
   shot 8, and each interior's last frame for the next.
4. **Regenerate by swapping only the subject sentence.** Leave the camera,
   lighting, style and palette lines exactly as they are. Editing those is how a
   shot silently leaves the film.
5. **Grade everything together at the end.** Even eight well-matched clips need
   one pass. If one came back warm or bright, fix it here rather than burning
   generations:

   ```bash
   ffmpeg -y -i out/shot_04.mp4 -vf "eq=saturation=0.85:contrast=1.08:gamma=0.95, \
   colorbalance=rs=-0.05:bs=0.08" -c:a copy out/shot_04_graded.mp4
   ```

6. **Assemble:**

   ```bash
   printf "file 'shot_%02d.mp4'\n" $(seq 1 8) > out/concat.txt
   ffmpeg -y -f concat -safe 0 -i out/concat.txt -c copy out/the_keeper.mp4
   ```

---

## Sound

Kling's text-to-video path won't give you dependable native audio, so this is an
edit job, not a prompt field. Which is good news — it's the cheapest place in the
whole film to carry meaning.

- **Bed:** low sea swell and wind, constant level under every shot, never ducking.
  Constant ambience across cuts is a continuity device in its own right; it glues
  clips that don't quite match.
- **Score:** one 30 Hz sub-bass drone entering at shot 4 and never leaving. Nothing
  else. No strings, no stingers.
- **Foley:** dry and close — boots on stone, the page turns in shot 4, the match in
  shot 7. Close foley against distant ambience is what makes a space feel real.
- **Shot 8:** half a second of total silence before the beam, then the wind
  returns without him in it.
- **No dialogue anywhere.**

---

## Files

- `KLING_PASTE.json` — the working document. Eight entries, each with a complete
  `paste` prompt and a matching `negative`. Nothing needs appending.
- `scenario.json` — the source. Edit this, not the JSON above.
- `build_kling.py` — rebuilds `KLING_PASTE.json` from `scenario.json`, merging the
  style and palette block into every shot mechanically. Run it after any edit;
  hand-merging is exactly where packages drift apart.

  ```bash
  python3 build_kling.py
  ```
