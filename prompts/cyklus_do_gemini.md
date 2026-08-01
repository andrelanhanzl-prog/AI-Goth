# KONEC CYKLU — prompty k vložení do Gemini

Osm záběrů po 8 sekundách = ~64 s filmu. Každý blok vlož do Gemini (Veo) **zvlášť**,
jeden po druhém, a výsledky pak slep za sebou v pořadí 1–8.

> Pozn.: Veo generuje 8s klipy. Delší film = generovat po záběrech a sestříhat.
> Pro plynulý přechod použij poslední snímek klipu jako vstupní obrázek dalšího
> (image-to-video), zvlášť mezi záběry 5 → 8.

---

## Globální styl (přidej na konec KAŽDÉHO promptu)

```
Style: cinematic 35mm anamorphic, shallow depth of field, heavy atmospheric haze,
fine film grain, slow deliberate camera, crushed blacks, desaturated midtones.
Palette: vacuum black, ember orange, bone white, cold cyan.
No text, no subtitles, no watermark, no logos, no UI, no cartoon or game render,
no distorted hands, no fast cuts, no lens flare spam, no flags, no real people.
```

---

## Záběr 1 — Poslední světlo

```
Extreme wide shot of a dying red star filling one third of the frame, its surface
churning in slow motion, shedding thin ribbons of plasma that dissolve into absolute
black. The star is visibly cooling, ember orange fading to dull brown at the edges.
No planets, no other stars, nothing else in frame. The camera drifts slowly backward
at a constant crawl, the star shrinking into an ocean of nothing.
Lighting: single practical source, no fill, extreme contrast.
Audio: 30 Hz sub-bass drone and one sustained cello note. No dialogue.
```

## Záběr 2 — Rozpad

```
Cosmic wide shot: a spiral galaxy slowly unwinding, its arms stretching apart like
smoke pulled by an invisible draft. Individual stars go dark one by one in a spreading
wave. The space between the stars visibly grows and cools to cyan-black. Billions of
years compressed into eight seconds, rendered smooth and silent, never frantic.
Camera: static wide with an almost imperceptible push-in.
Audio: granular white noise thinning out, drone falling in pitch. No dialogue.
```

## Záběr 3 — Druhý cyklus (match cut)

```
Night-time aerial of a vast city from high above, its roads and lights forming the
same spiral geometry as a galaxy, the ring road as a galactic arm. The city glows
ember orange. Slow aerial descent with a gentle yaw to the right. In the lower third
of frame whole districts blink out block by block in a spreading wave of darkness --
grids of streetlights and windows going out. In the still-lit parts traffic keeps
moving, unaware.
Audio: distant traffic hum, high-altitude wind, a held low drone. No dialogue.
```

## Záběr 4 — Setrvačnost

```
Street level at dusk turning to night. A dense crowd walks in one direction along a
wide boulevard, every face lit from below by the small screen they hold, everyone
moving at exactly the same pace, nobody looking up. Fine ash falls slowly like snow
and settles on their shoulders. Behind them a huge institutional building stands with
dark windows and a long crack running up its facade. Nobody reacts to the crack.
Camera: slow lateral tracking shot moving against the crowd, 50mm, shallow focus.
Audio: footsteps in perfect unison, muffled notification chimes, no voices.
```

## Záběr 5 — ROZCESTÍ (klíčový záběr)

```
The crowd is gone. A single solitary figure in a plain dark coat, seen from behind,
silhouetted, standing motionless at the point where the road splits into two paths.
The left path is cracked asphalt leading into low orange haze, burnt poles, a horizon
of smoke. The right path is the same asphalt with a hairline seam of green pushing
through it, leading toward a pale grey dawn. The figure does not move. The camera
does not move. Dust settles.
Lighting: warm orange from the left path, cool dawn from the right, the figure caught
exactly between them.
Camera: static locked-off wide, 35mm, the figure small and centred.
Audio: everything drops out except low wind and a single heartbeat every two seconds.
```

## Záběr 6 — Větev A: Popel

```
Slow forward travelling shot at walking pace through a landscape of collapsed
structures reclaimed by nothing at all -- no plants, no animals, only geometry and
ash. Half-buried machines, a toppled antenna mast, drifts of grey powder. Everything
is monochrome except one last ember glow on the horizon that is going out as we
watch. The frame gradually loses contrast and light until it is almost black.
Audio: wind through hollow metal, one distant structural groan, no music. No dialogue.
```

## Záběr 7 — Větev B: Klíček

```
One continuous shot with no cuts. Begin on extreme macro: a single green shoot pushing
up through a crack in dark asphalt, dew catching the first light. Pull back smoothly
to reveal many different hands, adult and child, working together to lift a broken
concrete slab. Keep pulling back to an extreme wide of a small settlement of low
buildings with lit windows, wind turbines turning slowly, terraced fields, and above
it a clear sky where new stars ignite one by one.
Lighting: true dawn, warm key from the horizon, soft bounce.
Audio: birds, distant human voices, strings entering in a major key.
```

## Záběr 8 — Nerozhodnuto (konec)

```
Return to the exact same framing as before: the solitary figure in the dark coat seen
from behind, standing at the fork between the burnt path and the dawn path. Nothing
has been decided. The figure lifts its head very slightly. The camera pushes in very
slowly toward the back of the head, and as it moves both paths blur out of focus until
only a single circular point of warm light remains in the centre of the frame. Hold on
that point of light. It does not go out. Cut to black on the last frame.
Camera: slow push-in, 85mm, focus racking from the paths to the single point of light.
Audio: wind of ash and birdsong layered at equal volume, then one low note, then silence.
```

---

## Proč to takhle funguje

| Záběr | Cyklus | Funkce |
|-------|--------|--------|
| 1–2 | vesmír | entropie, chladnutí, konec bez katastrofy |
| 3–4 | společnost | **stejný tvar, jiné měřítko** — spirála, vlna zhasínání, setrvačnost |
| 5 | — | rozhraní: dvě cesty, nikdo nerozhodl |
| 6 | popel | větev, kde setrvačnost vyhrála |
| 7 | klíček | větev, kde se cyklus otevřel znovu (nové hvězdy = obrácený záběr 2) |
| 8 | — | film **odmítne** rozhodnout; bod světla nezhasne |

Kruhový světelný zdroj je v každém záběru (hvězda, lampa, obrazovka, semínko,
zornice) a napříč filmem se zmenšuje — v posledním záběru se otevře znovu.
