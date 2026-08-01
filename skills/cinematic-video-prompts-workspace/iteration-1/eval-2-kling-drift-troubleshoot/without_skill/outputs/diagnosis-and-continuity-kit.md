# Why your 8 shots look like 8 different films
## Diagnosis + continuity kit — "The Keeper" (8-shot horror short, Kling)

---

## Part 1: What's actually going wrong

Short version: **you're generating each shot as a fresh text-to-video roll, so Kling is inventing a brand new world eight times.** Kling has no memory between generations. There is no project, no scene, no persistent set. Every "Generate" click is a coin flip in a slightly different universe.

Here's the breakdown by symptom:

### Symptom: "different color every clip"
**Cause:** Text-to-video color is a downstream side effect of thousands of unstated choices — time of day, implied film stock, implied grade. If your prompt doesn't nail the light *sources* and *color temperature in Kelvin*, the model picks. It picks differently every time.

**Also:** if you generated some clips on Kling 1.6 and some on 2.1/2.5, you're mixing models. They have visibly different color science. Never mix model versions within a short.

**Real fix:** lock the lighting logic in words (below), *and* accept that you finish the color in post. Nobody gets 8 matching grades out of a generator. You get 8 *close* grades and you unify them in Resolve. That's not a workaround, that's how it's done.

### Symptom: "the lighthouse changes shape"
**Cause:** You're re-describing the lighthouse in words in each prompt. Words are a lossy compression of a building. "A tall lighthouse on a rock" has a billion valid renderings and you're sampling from all of them.

**Also, specifically:** if you used red-and-white stripes or any countable feature, that's a guaranteed morph. Models cannot hold a stripe count. Same with window counts, railing spindles, signage text.

**Real fix:** stop describing it. Generate the lighthouse **once** as a still image, then use that image as the start frame for every exterior shot. Geometry is then literally identical because it's the same pixels.

### Symptom: "one came back looking like a cartoon"
**Cause:** Three usual suspects, probably all present:
1. **No start image.** Pure text-to-video has the widest style variance of anything Kling does. Illustration and 3D-render are enormous attractors in the training data.
2. **Creativity slider too high.** Kling's Creativity/Relevance control (sometimes shown as CFG) — if it's toward "creativity," you're explicitly asking it to wander. Push it toward relevance (~0.3 creativity) for a continuity-locked piece.
3. **Empty negative prompt.** You must actively push away from cartoon/anime/illustration/3D-render on every single generation. Kling's negative prompt field does not persist between generations in most UIs — it silently blanks. Check it every time.

### Symptom (the one you haven't noticed yet): prompt bloat in image-to-video
Once you switch to start frames, **long descriptive prompts become actively harmful.** If the image already shows a granite lighthouse and you also *describe* a granite lighthouse, the model tries to satisfy both and you get morphing, texture crawl, and drift.

In image-to-video the prompt's job is **motion only.** One or two sentences. What moves, how the camera moves, that's it.

This is the single most common mistake people make when they graduate from T2V to I2V.

---

## Part 2: The fix, as a workflow

You're changing from "write 8 prompts" to "build a set, then shoot on it." That's the whole shift.

### Step 1 — Build your reference plates (in a stills model, not Kling)
Use Midjourney, Flux, Nano Banana, Seedream, whatever you like. Make these, and only these:

| Plate | What it is | Used by shots |
|---|---|---|
| **A — Lighthouse exterior, night, wide** | Render this at max resolution. You will *crop into it* for every other exterior framing. | 1, 8 |
| **B — Keeper, 3/4 portrait, lantern-lit** | Your character lock. Face, sweater, everything. | 2, 5, 7 |
| **C — Keeper's kitchen/quarters interior** | Table, logbook, lantern, stone wall. | 2, 3 |
| **D — Spiral stone stair** | Curved wall, iron treads. | 4 |
| **E — Lamp room interior, dark** | The Fresnel lens, brass, dust, gallery window. | 5, 6, 7 |

Generate each plate with the **same style block** (Part 3) so the plates match each other. Iterate the plates until they're right — this is cheap, stills are fast. Do not move to Kling until all five plates look like they're from the same film.

**The crop trick:** render Plate A once at the highest resolution available. Your wide establishing shot and your final wide are then *crops of the same image*. The building geometry cannot drift, because it's one building.

**Character lock:** most stills tools now have a character-reference feature (`--cref` in MJ, reference image in Flux/Nano Banana). Make Plate B first, then use it as the character reference for C, D, E. Do not re-describe the keeper's face in words after Plate B exists.

### Step 2 — Shoot in Kling, image-to-video only
Every shot: upload the plate (or crop) as the **start frame**. Paste the short motion prompt. Paste the negative prompt. Generate.

Zero text-to-video. Not one shot.

### Step 3 — Pin your settings and never touch them
- **Model version:** pick one (Kling 2.5 Turbo or 2.1 Master) and use it for all 8. Mixing versions is the fastest way to break color continuity.
- **Mode:** Professional / Pro. Not Standard.
- **Duration:** 5s for all 8. Longer clips = more time for the model to drift and morph.
- **Aspect ratio:** pick one (I'd say 2.39:1 for this) and never change it.
- **Creativity/Relevance:** ~0.3 creativity / high relevance.
- **Negative prompt:** filled, every time, no exceptions. Re-check the field before every generation.

### Step 4 — Generate 3 variants per shot, keep the best match
Don't judge a variant on "is this good." Judge it on "does this cut against the shot before it." Continuity beats individual shot quality every time in a 40-second piece.

### Step 5 — Unify in post (non-optional)
In Resolve or Premiere:
1. **One grade node across all 8.** Match to your best shot, not to some ideal.
2. **One grain pass over everything** — grain is a phenomenal continuity glue. It hides an enormous amount of color and texture mismatch.
3. **Slight vignette on all 8.**
4. Conform everything to 24fps.

Steps 1–4 get you 85% matched. Step 5 gets you the rest. Anyone telling you they got 8 matching AI clips straight out of the box is not showing you the ones they threw away.

---

## Part 3: The locked blocks — paste these verbatim, never paraphrase

The rule: **these strings never change, in any shot, by even one word.** The moment you "improve" the style block for shot 5, shot 5 stops matching. Copy-paste discipline is the entire game.

### STYLE BLOCK
> Shot on 35mm anamorphic, 40mm lens, T2.8, shallow depth of field. Late-1970s North Atlantic coastal realism, photoreal live action. Available light only: a single kerosene lantern as the sole practical, warm 2200K, against moonless blue-black night ambience at 3200K. Desaturated palette limited to cold slate blue, wet black stone, and sodium-amber lantern glow — no other colour present. Heavy 35mm film grain, gate weave, crushed blacks, gentle halation on the lantern highlight, no lens flare.

### NEGATIVE PROMPT
> cartoon, anime, illustration, painting, drawing, 3D render, CGI, video game, stylised, plastic skin, waxy skin, oversaturated, teal and orange, lens flare, bloom, text, letters, watermark, logo, warped architecture, morphing, melting, extra fingers, deformed hands, fast camera movement, whip pan, zoom, drone shot, slow motion

### SUBJECT LOCK — THE KEEPER
> a gaunt man in his late fifties, hollow cheeks, grey stubble, deep-set tired eyes, thin hair wet-combed back, wearing a heavy charcoal wool sweater with a rolled collar under a dark oilskin jacket

### SUBJECT LOCK — THE LIGHTHOUSE
> a squat four-storey nineteenth-century lighthouse of unpainted grey granite, one narrow window per floor, a black iron gallery railing beneath an oxidised green copper lamp room dome, standing on black wet rock

Note what's **absent** from the lighthouse lock: no stripes, no paint scheme, no sign, no numbers. Everything countable or readable has been removed on purpose. Countable features are morph bait.

---

## Part 4: Triage for the clips you already have

Before you regenerate all eight, check:

- **Any clip that's close on framing but wrong on color** — keep it. Color is fixable in post. Don't burn credits.
- **Any clip where the lighthouse geometry is wrong** — regenerate from the plate. Not fixable.
- **The cartoon one** — regenerate. Start frame + negative prompt + relevance slider will kill it.
- **Any clip with a complex camera move** — check it for morphing at the end. Kling holds structure well for the first 2–3 seconds and gets loose after. If a clip is only good for 3 seconds, that's fine, cut it at 3 seconds. Most horror shots are better short anyway.

---

## Part 5: One story note

Your premise — *the light has been off for weeks* — has a built-in visual grammar you should exploit, because it also solves a technical problem.

The dramatic engine is **absence of light**, and absence of light means your entire short is lit by one lantern. One practical light source is the easiest thing in the world to keep consistent across generations. Your story constraint and your continuity constraint are the same constraint. Lean all the way into it: no moonlight, no second source, no ambient fill, no beam. Just the lantern and the dark.

And the horror beat is **dust.** Weeks of it. Dust is the evidence. When he finally gets up to the lamp room and the dust on the brass is thick and *undisturbed* — no footprints, no handprints, nothing touched — that's the shot the whole film is built to deliver. Shot 6 is your film. Protect it.

The 8 shots are in `shot-prompts.md`.
