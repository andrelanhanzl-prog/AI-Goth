# "The Keeper" — 8-shot prompt pack
## Image-to-video, Kling. Copy-paste ready.

**Total runtime: 40s (8 × 5s)**

---

## GLOBAL — set once, use on every shot

**Kling settings (identical for all 8):**
- Model: Kling 2.5 Turbo *(or 2.1 Master — pick one, never mix)*
- Mode: Professional
- Duration: 5s
- Aspect: 2.39:1
- Creativity: ~0.3 (high relevance)
- Input: **Image-to-video, start frame required. No text-to-video on any shot.**

**NEGATIVE PROMPT — paste into every generation, check the field each time:**
```
cartoon, anime, illustration, painting, drawing, 3D render, CGI, video game, stylised, plastic skin, waxy skin, oversaturated, teal and orange, lens flare, bloom, text, letters, watermark, logo, warped architecture, morphing, melting, extra fingers, deformed hands, fast camera movement, whip pan, zoom, drone shot, slow motion
```

**STYLE BLOCK — used to build the still plates. Do NOT paste into Kling motion prompts.**
```
Shot on 35mm anamorphic, 40mm lens, T2.8, shallow depth of field. Late-1970s North Atlantic coastal realism, photoreal live action. Available light only: a single kerosene lantern as the sole practical, warm 2200K, against moonless blue-black night ambience at 3200K. Desaturated palette limited to cold slate blue, wet black stone, and sodium-amber lantern glow — no other colour present. Heavy 35mm film grain, gate weave, crushed blacks, gentle halation on the lantern highlight, no lens flare.
```

**SUBJECT LOCKS — used in still plates only:**
- **KEEPER:** `a gaunt man in his late fifties, hollow cheeks, grey stubble, deep-set tired eyes, thin hair wet-combed back, wearing a heavy charcoal wool sweater with a rolled collar under a dark oilskin jacket`
- **LIGHTHOUSE:** `a squat four-storey nineteenth-century lighthouse of unpainted grey granite, one narrow window per floor, a black iron gallery railing beneath an oxidised green copper lamp room dome, standing on black wet rock`

**Reminder:** the Kling prompt describes **motion only.** The look is already locked by the start frame. Adding description fights the image and causes drift.

---

# SHOT 1 — THE DARK TOWER
*Establishing. The light is off, and we don't know it's wrong yet.*

**Start frame:** Plate A, full frame (uncropped).
Stills prompt: `Wide night shot from the sea, [LIGHTHOUSE], no light in the lamp room, black swell in the foreground, horizon barely separable from sky.` + STYLE BLOCK

**Kling motion prompt:**
```
Locked-off camera, no movement. Only the sea moves — a slow heavy swell rising and breaking against the black rock. The tower is completely still and completely dark.
```

**Note:** Kling will want to add camera drift. If variant 1 drifts, that's usually fine and even good — just don't let it drift toward the tower, which triggers geometry morph. Pick the stillest variant.

---

# SHOT 2 — THE ROUTINE
*He's fine. Everything's normal. He's been doing this a long time.*

**Start frame:** Plate C, keeper seated at the table, three-quarter back, lantern on the table beside an open logbook.
Stills prompt: `[KEEPER] seated at a small wooden table in a stone-walled room, seen from behind and to the side, writing in an open logbook, kerosene lantern on the table casting the only light, the room falling away into darkness.` + STYLE BLOCK

**Kling motion prompt:**
```
The man writes slowly in the logbook, his shoulder shifting with the pen. The lantern flame wavers once. The camera drifts a few inches closer.
```

**Note:** "a few inches" is deliberate. Kling responds well to small, physically stated camera moves and badly to "slow dolly in," which it over-interprets.

---

# SHOT 3 — THE PAGE
*Insert. The evidence is right there and he isn't reading it.*

**Start frame:** Plate C, cropped hard into the logbook. Shot from a low oblique angle so the handwriting is foreshortened and out of focus.
Stills prompt: `Extreme close-up of an open handwritten logbook on a wooden table, low oblique angle, handwriting illegible and soft-focused, lantern light raking across the paper from the left, deep shadow at the page edges.` + STYLE BLOCK

**Kling motion prompt:**
```
A hand enters frame and turns a single page. The page settles. The camera does not move.
```

**Note:** Keep the writing **illegible and out of focus** — this is non-negotiable. Legible text is where AI video falls apart hardest, and one garbled word breaks the film. Sell the "identical entries for weeks" idea through the *rhythm* of the handwriting and your sound design, not through readable dates.

---

# SHOT 4 — THE CLIMB
*Something makes him go up.*

**Start frame:** Plate D, from behind and below, keeper mid-stair with lantern raised.
Stills prompt: `[KEEPER] climbing a narrow spiral stone staircase, seen from behind and below, holding a kerosene lantern raised in his right hand, the curved granite wall lit in a moving pool of amber, blackness above and below him.` + STYLE BLOCK

**Kling motion prompt:**
```
He climbs. The pool of lantern light slides upward across the curved stone wall as he rises. The camera follows behind at his shoulder, unsteady.
```

**Note:** the sliding light on the curved wall is doing the work here — it reads as motion even if the figure animation is imperfect. If a variant has bad leg movement, crop tighter to the wall and the lantern.

---

# SHOT 5 — THE LAMP ROOM
*The reveal, part one. The lens is dark.*

**Start frame:** Plate E, keeper entering frame left from the stairwell, the great Fresnel lens dominating frame right, black and cold.
Stills prompt: `Interior of a lighthouse lamp room at night, a huge Fresnel lens filling the right of frame, unlit, black glass, [KEEPER] entering from the stairwell at frame left holding a kerosene lantern, brass fittings dull, the gallery windows beyond showing only darkness.` + STYLE BLOCK

**Kling motion prompt:**
```
He steps forward into the room and the lantern light spreads slowly across the black glass of the lens. He stops. Slow push in.
```

**Note:** the lens catching lantern light and *not* lighting up is your whole story beat. If a variant makes the lens glow or ignite, discard it immediately — no matter how pretty it is.

---

# SHOT 6 — THE DUST
*The reveal, part two. This is the shot the film is built for.*

**Start frame:** Plate E, cropped to macro on brass fittings under thick grey dust.
Stills prompt: `Macro shot of dull brass lighthouse fittings under a thick undisturbed layer of grey dust, raking lantern light from the left, black background, shallow focus.` + STYLE BLOCK

**Kling motion prompt:**
```
Fingertips enter frame and drag a single slow line through the thick dust. Dust lifts and turns in the light. The camera holds absolutely still.
```

**Note:** This is your best shot. Generate 5 variants of this one, not 3. What you want is *undisturbed* dust — no prior handprints, no footprints, nothing touched in weeks. Undisturbed dust is the answer to "how long has the light been off," and it lands without a single word of dialogue.

---

# SHOT 7 — THE COAST
*He looks out. It's worse than he thought.*

**Start frame:** Plate E, reframed to the gallery window, keeper in profile at the glass, black sea and black coastline beyond.
Stills prompt: `[KEEPER] in profile pressed close to a lighthouse gallery window at night, his face lit from below by the lantern in his lowered hand, the glass reflecting him faintly, beyond it a black coastline with no lights at all.` + STYLE BLOCK

**Kling motion prompt:**
```
He turns his head toward the window. The lantern in his hand lowers out of frame and his face falls into darkness. The camera does not move.
```

**Note:** the lantern lowering is a practical light cue Kling handles well, and it gives you a natural cut point — you can end the shot the instant his face goes black. Powerful, and it hides any facial drift in the back half.

---

# SHOT 8 — THE FIGURE
*Back where we started. Nothing has changed. That's the horror.*

**Start frame:** Plate A again — but crop slightly wider/further out than Shot 1, and composite or prompt a small motionless figure into the gallery.
Stills prompt: `Very wide night shot from far out at sea, [LIGHTHOUSE], no light in the lamp room, a small motionless human figure standing at the gallery railing, black swell filling the lower third of frame.` + STYLE BLOCK

**Kling motion prompt:**
```
The camera drifts slowly backward on the swell. The tower recedes. The figure at the railing does not move at all.
```

**Note:** Because this is the same source plate as Shot 1, your first and last shots will match perfectly — which makes the whole piece feel *designed* rather than assembled. Bookending with one plate is the cheapest continuity win available to you, and audiences read it as intent.

If the figure animates, regenerate. It must not move. That's the ending.

---

## Cut order and rhythm

```
1  THE DARK TOWER   5s   wide      — establish
2  THE ROUTINE      5s   medium    — normality
3  THE PAGE         5s   insert    — unread evidence
4  THE CLIMB        5s   tracking  — rising tension
5  THE LAMP ROOM    5s   medium    — reveal 1: it's dark
6  THE DUST         5s   macro     — reveal 2: for weeks
7  THE COAST        5s   profile   — reveal 3: nobody came
8  THE FIGURE       5s   very wide — resolve into dread
```

Shots 5–6–7 are your escalation and should cut fast and hard against each other. Shots 1 and 8 should feel long. If you have to trim, take frames off 2 and 4 — never off 6.

---

## Generation checklist (per shot)

- [ ] Start frame uploaded (never text-to-video)
- [ ] Motion prompt only — no style words, no subject description
- [ ] Negative prompt pasted and visible in the field
- [ ] Model version matches the other 7
- [ ] Duration 5s, aspect 2.39:1, Professional mode
- [ ] Creativity ~0.3
- [ ] 3 variants generated (5 for Shot 6)
- [ ] Variant chosen for **continuity with the neighbouring shot**, not standalone quality
