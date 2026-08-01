# Shot list and copy-paste prompts

**Assumption:** 90 in March means born around 1936, so she was ~20 in the autumn of 1956.
Adjust the age word in the subject string if that's off.

**Structure:** 8 AI shots at ~8 seconds = ~64s of material, cut down to ~52s, then her real
photograph and a title card. That's your minute.

Arc: *ordinary life → the world breaks → the decision → the leaving → the crossing → arrival
→ her, real, now.*

---

## The two strings you repeat verbatim

**SUBJECT STRING** (paste unchanged wherever she appears):

> a young woman of twenty in a brown wool coat with the top button missing, dark green
> headscarf over dark hair, carrying a small dark leather case

**STYLE BLOCK** — in `03-style-block.txt`. It is already appended to every prompt below.
If you edit it, edit it in all eight.

---

## Shot 1 — Before

*Ordinary morning. Establishes the world so we feel the loss of it.*

```
A quiet Budapest street on an ordinary morning in autumn 1956. A tram passes on wet
cobblestones. A few people in heavy coats walk to work, unhurried. Steam from a bakery
doorway. Nothing is wrong yet. Wide static shot from across the street.

Shot on grainy 16mm film, 1956 archival newsreel footage, recovered and slightly damaged.
Overcast winter light, flat and grey, no sun, no blue sky. Desaturated palette: slate grey,
olive brown, bone white, dull ochre. Low contrast, milky blacks, soft halation on the
highlights. Heavy fine grain, faint vertical scratches, slight gate weave and flicker.
Single fixed 35mm lens, soft at the edges. Camera handheld but slow and steady, near-static.
No zoom, no drone, no crane, no orbit, no slow motion, no lens flare, no rack focus.
Unglamorous and observational, nobody looks at the camera. Period-accurate 1950s Central
Europe. No text, no captions, no subtitles, no modern objects, no modern clothing.
```

## Shot 2 — The flag

*One image carries the whole revolution. The emblem cut out of the centre of the Hungarian
flag is the most recognisable symbol of 1956 and needs no explanation.*

```
A Hungarian tricolour flag hanging from a stone balcony, with a ragged hole cut out of its
centre where the emblem has been torn away. It moves slowly in a cold wind. Empty grey sky
behind it. Static shot, slightly low angle.

[STYLE BLOCK]
```

## Shot 3 — The street turns

*Aftermath, not violence. Seen from hiding — which is both truer and safer.*

```
View from inside a darkened doorway looking out at an empty city boulevard. Broken glass
and torn paper across the cobbles, an overturned cart, a burnt-out tram stopped at an angle.
Smoke drifts across the far end of the street. Nobody in sight. The camera stays in the
shadow of the doorway and does not go out. Static shot.

[STYLE BLOCK]
```

## Shot 4 — The decision

*Close, quiet, hands only. This is the emotional centre and the safest shot to generate —
no face to get wrong.*

```
Close shot of a woman's hands on a kitchen table, packing a small dark leather case by
lamplight. She puts in a folded photograph, a heel of bread wrapped in cloth, a pair of wool
stockings. Her hands stop for a moment, then close the case. We never see her face. Static
close shot, shallow focus.

[STYLE BLOCK]
```

## Shot 5 — Leaving

*Backs and distance. She's now defined by the coat.*

```
A crowded night railway platform in winter. Breath steams in the cold. a young woman of
twenty in a brown wool coat with the top button missing, dark green headscarf over dark hair,
carrying a small dark leather case walks away from camera into the crowd and is lost among
other coats. Shot entirely from behind at a distance. Static wide shot.

[STYLE BLOCK]
```

## Shot 6 — The crossing, first half

*The great escapes of 1956 happened on foot, at night, through the frozen marshes near the
Austrian border. Very wide, very small figures — the cheapest kind of consistency, because
at that scale there's almost nothing for the model to get wrong.*

```
Extreme wide shot at dusk. A line of six small distant figures walking single file through
flat frozen marshland, waist-high dead reeds, standing water, bare horizon. They are tiny in
the frame. No lights, no houses, no roads. Mist across the ground. Static wide shot.

[STYLE BLOCK]
```

## Shot 7 — The crossing, second half

*The threshold image. Hold this one longest.*

```
Night. A narrow wooden footbridge over a black drainage canal in open marshland. One person
carries a shielded lantern, low to the ground. Figures cross in silence one at a time, seen
from behind and at a distance. Reeds move in the wind. Static shot.

[STYLE BLOCK]
```

## Shot 8 — Arrival

*Resolution. Warmth, but not triumph. She is still only a coat and a back.*

```
Grey dawn on a muddy country road. a young woman of twenty in a brown wool coat with the top
button missing, dark green headscarf over dark hair, carrying a small dark leather case
stands with a blanket around her shoulders, seen from behind, watching the headlights of a
truck approach through the mist. Other figures wait nearby. Static wide shot.

[STYLE BLOCK]
```

---

## Shot 9 — Her

**Not generated.** A real scanned photograph of her, as young as you have. Hold it still,
long — five or six seconds, longer than feels comfortable. Optionally a very slow push in,
1–2% only.

If you have any photo of her at the age she was then, this is the shot the whole film is
built to arrive at. Everything before it is the setup.

## Shot 10 — Title card

Plain type, white on black, no animation:

```
[Her name]
left Hungary in 1956.
She is ninety today.
```

Then hold black for two seconds before it ends. Don't cut the black short — the room needs
a moment before anyone can clap.

---

## Cutting notes

- Order the clips, then trim each to its strongest 4–7 seconds. You will not use all 8
  seconds of anything.
- Aim for the film feeling *slow*. Shots 6 and 7 should be the longest.
- One sound bed under everything: wind, distant footsteps, a single sustained instrument.
  Let it run unbroken across every cut, including into the photograph.
- If you got her voice on tape, lay one or two short lines over shots 4 and 7 and let
  everything else be silent. Do not use her voice continuously — sparse is stronger.
- Music: something Hungarian and unadorned beats an orchestral score. Solo piano or a folk
  melody, low in the mix.

## If a shot fights you

- **It looks too clean / too modern:** the style block isn't dominating. Move it to the top
  of the prompt, and cut the scene description down — the more scene detail, the more the
  model wanders off-style.
- **The camera keeps moving:** add "locked-off tripod shot" and delete any verb in your
  scene description that implies motion.
- **She looks like a different person each time:** she's too close or too visible. Push her
  further away, put her back to camera, or cut to hands.
- **Two clips won't match no matter what:** stop prompting and fix it in the grade. That is
  the correct answer more often than not.
