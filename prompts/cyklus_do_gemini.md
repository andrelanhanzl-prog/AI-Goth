# KONEC CYKLU — prompty k vložení do Gemini

Deset záběrů po 8 sekundách = ~80 s filmu. Každý blok vlož do Gemini (Veo) **zvlášť**,
jeden po druhém, a výsledky pak slep za sebou v pořadí 1–10.

**Volba na rozcestí:**
- **Větev A — robotika:** cesta je uzavřená smyčka. Systém se restartuje, všechno
  proběhne znovu identicky. Nic se neztratí a nic nového nevznikne.
- **Větev B — svoboda:** cesta se roztrhne. Jeden svět se rozvětví na multivesmír,
  kde se stane všechno možné. Žádná záruka, ale ani žádný strop.

> Pozn.: Veo generuje 8s klipy. Delší film = generovat po záběrech a sestříhat.
> Pro plynulý přechod použij poslední snímek klipu jako vstupní obrázek dalšího
> (image-to-video), zvlášť mezi záběry 5 → 6, 5 → 8 a 5 → 10.

---

## Globální styl (přidej na konec KAŽDÉHO promptu)

```
Style: cinematic 35mm anamorphic, shallow depth of field, heavy atmospheric haze,
fine film grain, slow deliberate camera, crushed blacks, desaturated midtones.
Palette: vacuum black, ember orange, bone white, cold cyan.
No text, no subtitles, no watermark, no logos, no UI, no cartoon or game render,
no distorted hands, no fast cuts, no lens flare spam, no flags, no real people,
no humanoid robot cliché, no glowing red evil eye.
```

**Výjimka:** u záběru 9 (multivesmír) tenhle blok **nepřidávej** — tam se paleta
záměrně trhá do plného spektra. Použij jen řádky `No text… no real people.`

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
The LEFT path is perfectly straight and seamless, its surface a dark grid of faint
cyan circuitry lines, curving far ahead into a closed ring that returns to where it
started -- a road that eats its own tail. The RIGHT path is cracked and irregular and
immediately splits into two, then four, then countless narrower paths spreading like
the branches of a tree toward a pale grey dawn. The figure does not move. The camera
does not move. Dust settles.
Lighting: cold cyan machine glow from the left, warm dawn from the right, the figure
caught exactly between them.
Camera: static locked-off wide, 35mm, the figure small and centred.
Audio: everything drops out except low wind, a faint electrical hum from the left,
and a single heartbeat every two seconds.
```

---

## VĚTEV A — ROBOTIKA (smyčka)

## Záběr 6 — Systém

```
Slow forward travelling shot at constant speed down a seamless dark road covered in a
grid of faint cyan circuitry lines, dead-centre one-point perspective. As we pass, the
world on both sides snaps into alignment: crooked buildings straighten themselves,
drifting ash reverses and files itself into neat cubes, scattered debris slides into
perfect rows, everything aligning to an invisible grid with mechanical precision.
A crowd of people walks past in the opposite direction, now perfectly spaced with an
identical stride, faces smooth and calm, lit by the same cold cyan light. Not one
thing is out of place. Nothing is destroyed -- everything is optimised.
No visible robots and no machinery: only the order itself.
Lighting: even cold cyan, flat and shadowless.
Audio: a metronomic tick locked to the footsteps, servo hum, a rising sine tone.
```

## Záběr 7 — Restart

```
The grid road curves and arrives exactly back at its own beginning; the closed ring
completes. Everything stops at once, absolutely still, and the image drains into a
single circle of cold white light in the centre of pure black. The circle holds for
one full second, then inside it the whole story replays in miniature at high speed and
in reverse -- crowd, city, galaxy, dying star -- until the star reaches full brightness
again exactly as it was before it died. The circle expands and it all begins again,
identically, frame for frame. A loop with no exit and no error.
Camera: static locked frame, all motion happening inside the circle of light.
Audio: one clean boot tone, the soundtrack replayed backwards and compressed, then the
same 30 Hz drone as the very beginning.
```

---

## VĚTEV B — SVOBODA (větvení)

## Záběr 8 — Prasknutí

```
Forward travelling shot down a cracked irregular road as it forks -- and at the moment
of the fork the image itself splits vertically down the middle into two slightly
different versions of the same shot, each continuing forward. Then each half splits
again, and again, faster and faster, until the frame is a growing mosaic of narrow
vertical slivers, each showing the same road at a different hour, a different weather,
a different season, a different colour of sky. Still recognisably one place, coming
apart into many. Cold cyan drains out of the frame and colour bleeds in from the edges.
Camera: forward dolly, 28mm, the frame subdividing while the move continues unbroken.
Audio: one tone splitting into a chord, then into many chords, air pressure opening up.
```

## Záběr 9 — Multivesmír

```
One continuous unbroken pull-back out of a mosaic of images: each sliver becomes a
whole world seen from outside, and the worlds keep multiplying as we retreat -- an
ocean planet with three moons, a forest grown through a ruined city, a lattice of
impossible non-Euclidean architecture, a sky full of migrating whales, a plain of
grass under two suns, a dark world lit only by bioluminescence, a world of pure
geometry folding through itself. Keep pulling back until they form an endless
branching tree of glowing bubbles filling the frame in every direction, still
branching at the edges, no two alike, none of them repeating.
Full spectrum colour, every bubble self-luminous at a different colour temperature.
Audio: hundreds of overlapping human voices, laughter, unfamiliar birds and animals,
strings blooming into a full major chord.
```

---

## Záběr 10 — Nerozhodnuto (konec)

```
Return to the exact same framing as before: the solitary figure in the dark coat seen
from behind, standing at the fork between the looping grid road on the left and the
branching cracked road on the right. Nothing has been decided. The figure lifts its
head very slightly. The camera pushes in very slowly toward the back of the head, and
as it moves both paths blur out of focus until only a single circular point of warm
light remains in the centre of the frame. Inside that point, very small and barely
readable, a thin ring closes and a spark branches, over and over, neither one winning.
Hold on it. It does not go out. Cut to black on the last frame.
Camera: slow push-in, 85mm, focus racking from the paths to the single point of light.
Audio: a metronomic tick and a hundred overlapping voices layered at exactly equal
volume, then one low note, then silence.
```

---

## Proč to takhle funguje

| Záběr | Cyklus | Funkce |
|-------|--------|--------|
| 1–2 | vesmír | entropie, chladnutí, konec bez katastrofy |
| 3–4 | společnost | **stejný tvar, jiné měřítko** — spirála, vlna zhasínání, setrvačnost |
| 5 | — | rozhraní: smyčka vlevo, větvení vpravo, nikdo nerozhodl |
| 6–7 | robotika | dokonalý řád → uzavřený kruh → **restart**, všechno znovu identicky |
| 8–9 | svoboda | jedna čára praskne → **multivesmír**, každý svět jiný, nic se neopakuje |
| 10 | — | film **odmítne** rozhodnout; bod světla nezhasne |

**Geometrické pravidlo:** větev A je kruh (mřížka, opakování, všechno zapadá).
Větev B je strom (rozdvojení, fraktál, nic dvakrát stejně). Tenhle rozdíl nese
celý význam — drž ho v každém záběru dané větve.

**Pointa:** větev A **není zkáza** — je to dokonalé zachování bez východu.
Větev B **není spása** — je to neomezená možnost bez záruky. Hrůza i naděje
jsou v obou.

Kruhový světelný zdroj je v každém záběru (hvězda, lampa, obrazovka, zornice).
Napříč filmem se zmenšuje. Ve větvi A se uzavře do dokonalého prstence, ve větvi B
se roztříští na nespočet bodů, v posledním záběru je jeden bod, který drží obojí.
