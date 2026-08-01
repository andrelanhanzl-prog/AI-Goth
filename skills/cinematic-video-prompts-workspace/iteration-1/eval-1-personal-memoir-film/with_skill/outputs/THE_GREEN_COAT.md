# The Green Coat — a one-minute film for a 90th birthday

**Spine.** In November 1956 a young woman takes a coat off a hook in Budapest and
walks out of Hungary. Seventy years later the same coat hangs in a kitchen full of
people who exist because she did.

What is true at the end that wasn't true at the start: the room is full.

**Runtime.** 8 shots × 8s = 64s of generated material. Trim each clip to about 7
seconds in the edit and you land at 56s, leaving room for the last 4 seconds, which
should not be generated at all — see [The ending](#the-ending-dont-generate-it).

---

## The one thing you asked about

Your worry — "every clip is going to look like a different movie" — is the correct
worry, and it is not mainly solved by prompting. It's solved in this order:

1. **One continuous piece of music across the whole minute.** Mute every clip's
   generated audio. A single unbroken music bed is the strongest continuity device
   available to you and it costs nothing. Eight clips under one piece of music read
   as one film even when they shouldn't.
2. **One grade pass over all eight clips at the end.** Same colour correction
   applied to everything. Recipe below.
3. **An anchor object described identically in every prompt** — here, the coat.
4. **The same style and palette sentence, byte-for-byte, in every prompt.** This is
   what `SORA_PASTE.json` is for: the sentences were merged in by script, not by
   hand, so no shot can quietly drift.
5. **No faces anywhere in the film.** More on this below — it's the single biggest
   source of "different movie" and it is entirely avoidable here.

Prompting is item 3 and 4 on that list. Do 1 and 2 as well or the prompting won't
save you.

---

## The consistency anchor

**A dark green wool overcoat with a hand-stitched grey repair on the left cuff.**

It is in every shot, and its condition is the film's clock:

| Shot | State of the coat |
|---|---|
| 1 | Clean, hanging on an iron hook |
| 3 | On her back, under a streetlamp |
| 4 | Mud caked to the knee |
| 6 | Soaked, frozen, in marsh water |
| 7 | Steaming in a warm doorway |
| 8 | Clean, hanging on an iron hook |

That's the whole film in six lines. If a regenerated clip has the wrong coat, throw
the take away — it is the one thing worth being strict about.

There's a second, quieter anchor: the **light**, which travels warm lamp → grey
overcast → one streetlamp → one torch beam → moonlight → warm and cold meeting at a
threshold → full daylight. If a take fights that sequence it's the wrong take.

---

## The no-faces rule

You cannot get your grandmother's face out of Sora. Not at 20, not at all — it
won't reproduce a real person's likeness on request, and the near-misses it *does*
produce are exactly the kind of thing that lands badly in a room full of people who
know her face. It would also give you eight different women across eight clips,
which is your original worry in its worst form.

So the film is shot **entirely from behind, beside, and below her.** Hands, the back
of a head in silhouette, a coat hem, boots, a tiny figure at distance. No clear face
in any of the eight shots.

Treat that as a style, because it is one — a film that follows someone rather than
looks at them is a real choice, and here it happens to also be the choice that works.
Her actual face belongs in the edit, from photographs.

---

## Shot list

| # | Title | Job | Note |
|---|---|---|---|
| 1 | The hook | Establish | Anchor introduced |
| 2 | The street after | Escalate | Aftermath, no violence |
| 3 | Looking back at the city | Rhyme A | She leaves |
| 4 | Night walking | Time passing | Coat takes damage |
| 5 | The marsh | Peak | One person, whole landscape |
| 6 | The turn | **The turn** | Rhyme A repeated, one country later |
| 7 | The door | Arrival | Warm and cold meet at a threshold |
| 8 | The same hook | Pay off | Rhyme B — shot 1 repeated, in colour, now |

Two structural things hold it together:

- **Shots 3 and 6 share a camera line word for word.** Same framing, same distance,
  same gesture — she turns her head and looks back. Once at a streetlamp, once in a
  marsh. Do not paraphrase the second one. The audience does the emotional work.
- **Shots 1 and 8 share a camera line word for word.** A coat on a hook, then a coat
  on a hook. Everything between them happened.

**Shot 8 deliberately breaks the look.** Shots 1–7 are desaturated 16mm with a
locked palette; shot 8 is clean modern digital, full colour, and carries the film's
first saturated red on the party table. That's the point — the past looks like the
past and the present looks like now. Don't "fix" it to match.

---

## The prompts

Each one is complete. Paste it on its own; nothing needs appending. The
paste-ready versions are in `SORA_PASTE.json` — these are the same strings laid out
so you can direct from them.

### Shot 1 — The hook

> A woman's hands lift a heavy dark green wool overcoat off an iron hook on the back
> of an apartment door in Budapest in November 1956. The coat has a hand-stitched
> grey repair on the left cuff. She holds the coat still for a moment before pulling
> it down off the hook. Her face is never in frame.
>
> **Camera:** static locked-off medium, 50mm, framed square on the door with the hook
> at chest height, no camera movement.
> **Lighting:** single warm table lamp behind camera, no fill, the top corners of the
> door falling into deep shadow.
> **Style:** 1956 archival feel, 16mm film grain, halation blooming on the highlights,
> slight gate weave, shallow depth of field, desaturated muted grade, 16:9.
> **Palette:** wet slate grey, dirty snow white, lamp amber, marsh brown, cold moon blue.
> **Audio:** a clock ticking in the next room, faint street noise muffled through
> glass, one unaccompanied violin note held underneath, no dialogue.
> **Avoid:** text, subtitles, captions, watermarks, logos, interface elements,
> distorted hands, extra limbs, fast cuts, camera shake, handheld jitter, faces in
> close-up, modern clothing, modern cars, plastic, mobile phones, saturated red,
> swastikas, Nazi imagery, World War Two uniforms, weapons, blood, gore, other people
> in frame, packed suitcases piled up, propaganda posters.

### Shot 2 — The street after

> An empty Budapest boulevard at first light seen from the middle of the road. A tram
> stands stopped and abandoned on its rails with both doors open. Shattered shop glass
> lies across the wet cobblestones and loose paper leaflets drift slowly along the
> gutter. There are no people anywhere in the frame.
>
> **Camera:** static locked-off extreme wide, 28mm, one-point perspective straight down
> the tram rails, horizon locked, no camera movement.
> **Lighting:** flat grey overcast dawn, no visible sun, low contrast everywhere except
> the black interior of the tram.
> **Style / Palette:** as shot 1.
> **Audio:** wind, loose paper scraping over stone, a distant unattended tram bell, no
> dialogue.
> **Avoid:** the shared list, plus crowds, soldiers, tanks, fire, explosions, rubble
> piles, bodies.

This shot says why she is leaving without showing anything that happened. An empty
tram with its doors open does more than a tank, and it won't trip Sora's content
filters or turn a birthday film into a war film.

### Shot 3 — Looking back at the city

> A woman in a dark green wool overcoat with a hand-stitched grey left cuff stands
> under a streetlamp at the edge of an empty Budapest square, seen from directly
> behind, and slowly turns her head to look back down the street she came from. She is
> in silhouette and her face is not visible at any point.
>
> **Camera:** static locked-off wide from directly behind her at her shoulder height,
> 50mm, the figure small in the lower third of the frame, no camera movement.
> **Lighting:** one overhead streetlamp directly above her throwing a hard pool of
> amber light, everything beyond the pool completely black.
> **Style / Palette:** as shot 1.
> **Audio:** her boots on wet stone, then silence, one low sustained cello note, no
> dialogue.
> **Avoid:** the shared list, plus other pedestrians, car headlights, her face turning
> fully to camera.

### Shot 4 — Night walking

> The hem of a dark green wool overcoat and a pair of worn leather boots walking
> through frozen mud in the dark, a small cardboard suitcase swinging at knee height
> beside them. Mud is caked up the coat to the knee. Nothing above the waist is
> visible and nothing beyond a couple of metres is visible.
>
> **Camera:** steady low tracking shot at ankle height moving backwards ahead of her at
> walking pace, 35mm, shallow depth of field.
> **Lighting:** one weak handheld torch beam entering from off-frame and raking across
> the mud, everything past two metres in total darkness.
> **Style / Palette:** as shot 1.
> **Audio:** boots pulling out of thick mud, steady breathing, wind in dry grass, no
> dialogue.
> **Avoid:** the shared list, plus faces, other walkers, paved roads, streetlights.

The darkness is doing real work: it's the one shot where you're asking for walking
motion, and limiting visibility to two metres gives the model almost nothing to get
wrong.

### Shot 5 — The marsh

> An extreme wide of a flat frozen border marsh under an enormous night sky, reeds
> standing taller than a person, and one tiny distant figure in a dark overcoat wading
> through shallow water far away in the middle of the frame. Two faint torch beams
> sweep along the horizon behind her.
>
> **Camera:** static locked-off extreme wide, 24mm, horizon locked in the lower quarter
> of the frame, no camera movement.
> **Lighting:** cold moonlight from high camera left, the distant figure backlit and
> completely black, mist glowing where the moonlight passes through it.
> **Style / Palette:** as shot 1.
> **Audio:** water moving around legs, reeds knocking together, a dog barking a long way
> off, a low sub-bass drone, no dialogue.
> **Avoid:** the shared list, plus soldiers, dogs in frame, gunfire, weapons, searchlight
> towers, barbed wire in close-up, boats, buildings.

The torch beams and the far-off dog carry the entire danger of the crossing. Nothing
threatening is ever in frame, which is both truer and far more reliable to generate.

### Shot 6 — The turn

> A woman in a dark green wool overcoat with a hand-stitched grey left cuff stands
> still in shallow marsh water, seen from directly behind, and slowly turns her head to
> look back the way she came. Her breath is visible in the cold. Her face is not
> visible at any point. She is the only thing in the frame that is not landscape.
>
> **Camera:** static locked-off wide from directly behind her at her shoulder height,
> 50mm, the figure small in the lower third of the frame, no camera movement.
> **Lighting:** cold moonlight from high camera left, a hard rim of light on one shoulder
> only, everything ahead of her black.
> **Style / Palette:** as shot 1.
> **Audio:** wind in reeds, one long breath, an unaccompanied violin note held a beat too
> long, no dialogue.
> **Avoid:** the shared list, plus her face turning fully to camera, other figures,
> torchlight hitting her, buildings.

The camera line is copied from shot 3 on purpose. Hold this one the longest in the
edit — it is the moment the film is about, and it should feel slightly too long.

### Shot 7 — The door

> A farmhouse door in rural Austria swings inward at grey dawn and warm interior light
> falls across a pair of mud-caked leather boots and the frozen hem of a dark green
> wool overcoat standing on the step outside. A stranger's hand comes into the light
> holding out an enamel mug. No faces are visible.
>
> **Camera:** static locked-off low medium, 40mm, framed on the doorstep from inside the
> house looking out, no camera movement.
> **Lighting:** warm interior lamplight spilling from behind camera onto the step, cold
> blue dawn beyond the door, the two colours meeting exactly at the threshold.
> **Style / Palette:** as shot 1.
> **Audio:** a door hinge, wind cutting off as the door opens, a kettle somewhere inside,
> the violin resolving onto a second note, no dialogue.
> **Avoid:** the shared list, plus faces, welcome signs, flags, uniformed officials,
> paperwork.

Warm light and cold light meeting on a doorstep is the whole of 1956 in one frame.
Nobody needs to explain it.

### Shot 8 — The same hook, seventy years later

> The same dark green wool overcoat with a hand-stitched grey repair on the left cuff
> hangs on an iron hook on the back of a door in a warm modern family kitchen. Beyond
> it and out of focus a long table is being laid for a party and someone walks past
> carrying a cake. No faces are visible. Style: clean modern digital capture, no film
> grain, natural colour, shallow depth of field, 16:9. Palette: warm daylight white,
> oak brown, and one deep saturated red on the party table.
>
> **Camera:** static locked-off medium, 50mm, framed square on the door with the hook at
> chest height exactly as in the first shot, one slow focus rack from the coat to the
> room behind it.
> **Lighting:** bright soft daylight through a large window camera right, warm and even,
> no hard shadow anywhere on the coat.
> **Audio:** indistinct warm room tone of many people talking with no intelligible words,
> cutlery on plates, the violin joined by a second violin, no dialogue.
> **Avoid:** text, subtitles, captions, watermarks, logos, interface elements, distorted
> hands, extra limbs, fast cuts, camera shake, handheld jitter, faces in close-up, film
> grain, sepia, vintage look, banners with lettering, numerals, balloons or candles
> spelling a number, party hats, faces.

The film's only camera move is the focus rack in this shot, pulling from the coat to
the room. Save all your movement for the last eight seconds and it means something.

---

## What Sora will not do, and what to do instead

| The ask | Why it fails | Simplified route (in the prompts) | Compositing route |
|---|---|---|---|
| Her actual face | Sora won't render a real person's likeness, and eight generations give you eight different women | No faces anywhere; follow her from behind | Real photographs in the edit — see below |
| The coat being *identical* in all 8 clips | The model has never seen the other clips | The hand-stitched grey left cuff, described in identical words every time | Frame-chain the seams; then a shared grade pass hides the rest |
| The shot 3 / shot 6 rhyme | The model never saw shot 3 | Copy the camera line word for word | Generate 6 as a remix/extension of the shot 3 clip if your plan has image input |
| "90", a date, a Hungarian street sign | Legible text is still unreliable and often comes out as garbled pseudo-letters | `text` is in every avoid list | Add every word in your editor. Titles are free and perfect there |
| 200,000 refugees, the scale of the exodus | Unbounded crowds collapse into repeated bodies and melted faces | One figure in one enormous landscape (shot 5) | Don't. One person is the correct scale for this film anyway |
| Period-correct trams, signage, vehicles | The model drifts, and reliably confuses mid-century Eastern Europe with WWII | Keep vehicles distant, still, and out of focus; `World War Two uniforms, swastikas` in the avoid list | Crop in, or blur, in the editor |

If any clip comes back with a swastika or a soldier, that's the known WWII conflation
— regenerate rather than trying to reword. It's a coin flip, not a prompt problem.

---

## The ending — don't generate it

The last four seconds should be **a real photograph of her at around twenty**, held
still, with a very slow push in, and then black.

Nothing Sora makes will beat that, and after 56 seconds of never seeing her face,
seeing it is the entire payoff. If you have a photograph of her arriving, or her
papers, or a ship or plane ticket, that works too. Scan at the highest resolution
you can and let it sit there.

**The optional version that will destroy the room:** record her, on your phone,
telling twenty seconds of it in her own words. Then lay her voice over shots 4 to 7
and drop the music down underneath. You do not need her to narrate the whole thing
— one sentence, in her own voice, over the marsh, is enough. Ask her before March.
That's the film; the generated part is the illustration.

---

## Assembling it

**Generate in this order:** 1, then 8 (so you can compare the two hook framings
immediately and regenerate whichever is worse), then 3, then 6, then the rest. Get
the two rhyming pairs right before you spend credits on the middle.

**Hold fixed across all eight:** same aspect ratio (16:9 for a TV at a party), same
model, same resolution, same seed if Sora exposes one. Change nothing but the prompt.

**Generate at Sora's longest available clip length and trim.** These prompts hold
about 8 seconds of content. If the clip is longer than the content, the model invents
a second event to fill it — a second person walks in, the camera starts moving. Trim
in the editor instead.

**Check the watermark before you build the edit.** Depending on your Sora plan,
downloads may carry a moving watermark. Find out on your first clip, not on your
eighth — it changes whether you can project this.

**Frame-chain the two seams that matter,** if your plan offers image input: the last
frame of shot 5 as the opening image of shot 6 (same marsh, must persist), and a
frame of the coat from shot 1 as reference for shot 8.

```bash
ffmpeg -y -sseof -0.1 -i shot_05.mp4 -frames:v 1 shot_05_last.png
```

**Then, in order:**

```bash
# 1. one shared grade over every clip — this is the big one
for f in shot_0*.mp4; do
  ffmpeg -y -i "$f" -vf "eq=saturation=0.88:contrast=1.06:gamma=0.97, \
    colorbalance=rs=-0.04:bs=0.06" -an "graded_$f"
done

# 2. stitch
printf "file 'graded_shot_%02d.mp4'\n" $(seq 1 8) > concat.txt
ffmpeg -y -f concat -safe 0 -i concat.txt -c copy film_silent.mp4

# 3. lay one continuous music track over the whole thing
ffmpeg -y -i film_silent.mp4 -i music.mp3 -c:v copy -shortest film.mp4
```

Note the `-an` in step 1 — it strips Sora's generated audio. Do that. The generated
audio is per-clip and per-clip audio is what makes eight clips sound like eight
clips. Keep shot 8's room tone if you like it, laid in separately at low level.

For music: one solo instrument, unaccompanied, that plays continuously across all
sixty seconds. A single violin or a solo piano. Anything with a drum kit will fight
the images.

---

## Before you start: four things to check with her

Shots 2, 3, 5 and 7 assume the common route — Budapest, then the border marshes near
Andau, then an Austrian farmhouse. Roughly 200,000 people left that way in the winter
of 1956, so it may well be hers. But it might not be.

Ask her, and if it differs, change those four prompts in `scenario.json` and rerun:

```bash
python build_paste.py scenario.json -o SORA_PASTE.json
```

1. **Where did she leave from** — Budapest, or a village? (shots 1–3)
2. **How did she cross** — on foot through the marshes, by train, hidden in a
   vehicle? (shots 4–5)
3. **What did she carry**, and what was she wearing? If there's a real coat, or a
   real bag, put *that* in the anchor instead of the green one. (all shots)
4. **Where did she arrive first** — a farmhouse, a camp, a station? (shot 7)

Every one of those answers makes the film better than the generic version, and
asking is a good thing to be doing in the weeks before her ninetieth anyway.

---

## Files

- `SORA_PASTE.json` — paste-ready. Eight complete prompts, nothing to append.
- `scenario.json` — the source. Edit this and rerun `build_paste.py` rather than
  editing the paste file by hand; hand-editing is exactly how one shot drifts.
- `THE_GREEN_COAT.md` — this document.
