# Záběry 7, 9, 10 — proč selžou a čím je nahradit

Tyhle tři záběry po Veo chtějí něco, co generativní model z jednoho 8s promptu
neudrží. Každý má níž **variantu A** (jeden prompt, zjednodušený tak, aby prošel)
a **variantu B** (rozdělit na díly a složit v postprodukci — vyjde to líp).

---

# ZÁBĚR 7 — Restart

**Proč selže:** chceš po něm přehrání celého filmu pozpátku uvnitř kroužku světla.
To je kompozice, ne generace. Veo nemá ponětí, co bylo v předchozích klipech —
vygeneruje „nějaké abstraktní blikání v kruhu“ a rytmus restartu se ztratí.

## Varianta A — jeden prompt (bezpečná, slabší)

```
Static locked frame. A seamless dark road covered in a grid of faint cyan circuitry
lines curves and arrives back at its own starting point, closing into a perfect ring.
The instant the ring closes, all motion stops at once and the entire image drains
inward into a single small circle of cold white light in the centre of pure black.
The circle holds perfectly still, pulses once, then expands smoothly outward until it
fills the frame with white. No text, no numbers, no interface.
Audio: one clean boot tone, a fast descending sweep, then a 30 Hz sub-bass drone.
```

Bílá expanze na konci je střihový můstek — navazuje přímo na záběr 1.

## Varianta B — poskládat v ffmpegu (doporučeno)

Nenech to generovat. Vezmi **už hotové klipy 1–4**, pusť je pozpátku, zrychli a
promítni je dovnitř kruhu z varianty A. Restart tím doslova *je* tvůj vlastní film:

```bash
# 1) klipy 1-4 za sebou, pozpátku, 8x zrychleně -> ~4 s
ffmpeg -y -f concat -safe 0 -i out/concat.txt -c copy out/_a.mp4
ffmpeg -y -i out/_a.mp4 -vf "reverse,setpts=PTS/8" -an out/_rev.mp4

# 2) maska kruhu + vložení do středu černého pole
ffmpeg -y -i out/shot_07.mp4 -i out/_rev.mp4 -filter_complex \
"[1:v]scale=360:-1,format=rgba, \
 geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':\
a='if(lte(hypot(X-W/2,Y-H/2),H/2),255,0)'[disc]; \
 [0:v][disc]overlay=(W-w)/2:(H-h)/2:enable='between(t,1,5)'" \
-c:a copy out/shot_07_final.mp4
```

`enable='between(t,1,5)'` = kruh je prázdný první sekundu (ticho), pak se v něm
převine film, pak zase prázdno a expanze do bílé. Ten rytmus **ticho → převinutí →
znovu** je celý smysl záběru.

---

# ZÁBĚR 9 — Multivesmír

**Proč selže:** „nekonečně se větvící strom světů, žádné dva stejné“ je přesně to,
v čem se video modely rozpadají — udělají opakující se kaši z bublin. A pull-back
z makra až do nekonečna je moc velký rozsah měřítek na 8 sekund.

## Varianta A — jeden prompt (méně světů, konkrétně pojmenované)

Nechtěj nekonečno. Chtěj **pět konkrétních světů** — mozek si nekonečno domyslí sám.

```
One continuous unbroken pull-back. We start close on a single glowing sphere holding
a whole world inside it: an ocean planet with three moons. As the camera retreats,
four more spheres drift into frame around it, each holding a completely different
world -- a forest grown through a ruined city, a plain of grass under two suns, a dark
world lit only by turquoise bioluminescence, a lattice of impossible folding geometry.
Keep retreating; the five become twenty, then hundreds, receding into depth in every
direction like a slow snowfall of luminous worlds, softly out of focus at the edges.
Full spectrum colour, every sphere self-luminous at its own colour temperature.
Camera: slow continuous pull-back, no cuts, no camera shake.
Audio: overlapping human voices and laughter, unfamiliar birds, strings blooming into
a full major chord.
```

Klíčové je **„softly out of focus at the edges“** — rozostření okrajů model zbaví
nutnosti kreslit tisíc detailních světů a zároveň to vypadá nekonečně.

## Varianta B — dva klipy (doporučeno)

- **9a — Prasknutí do mozaiky** (dojezd záběru 8): rám se dělí na svislé pruhy,
  z každého je jiný svět. 8 s.
- **9b — Oceán světů**: čistý pull-back z bublin do hloubky, bez dělení rámu. 8 s.

Rozdělením zbavíš model dvou úkolů naráz. Střih mezi 9a a 9b schovej do momentu,
kdy je frame nejvíc rozdrobený — tam si nikdo ničeho nevšimne.

**Když chceš víc rozmanitosti:** vygeneruj 3–4 samostatné 2s klipy jednotlivých
světů a nasaď je do mozaiky přes `overlay` stejně jako u záběru 7. Rozmanitost
tak nedělá model, ale střih — a ta je pak skutečná.

---

# ZÁBĚR 10 — Nerozhodnuto

**Proč selže:** „uvnitř bodu světla se zavírá prstenec a větví jiskra“ je pod
rozlišením. Veo tam nacpe buď nečitelnou skvrnu, nebo — a to je horší — udělá z toho
velký zřetelný symbol a **tím tu volbu rozhodne za diváka**. Přesně to, co film nesmí.

## Varianta A — vyhoď to z promptu

Nech tam jen ten bod. Dvojznačnost unese **zvuk**, ne obraz:

```
A solitary figure in a plain dark coat seen from behind, silhouetted, standing
motionless at a fork where a smooth grid road curves away to the left and a cracked
branching road spreads away to the right. The figure lifts its head very slightly.
The camera pushes in very slowly toward the back of the head; as it moves, both paths
blur completely out of focus until only a single small circular point of warm light
remains in the centre of the frame. It holds steady. It does not go out.
Camera: slow push-in, 85mm, focus racking from the paths onto the point of light.
Audio: a steady metronomic mechanical tick and a hundred overlapping human voices,
layered at exactly equal volume, then one low note, then silence.
```

Ten stejně hlasitý tikot a hlasy jsou celé rozhodnutí. Nic víc není potřeba.

## Varianta B — prstenec a jiskra jako overlay

Když to tam chceš mít, přidej to v postprodukci — malé, na hranici viditelnosti:

```bash
ffmpeg -y -i out/shot_10.mp4 -i assets/ring_spark.mov -filter_complex \
"[1:v]scale=48:48,format=rgba,colorchannelmixer=aa=0.55[fx]; \
 [0:v][fx]overlay=(W-w)/2:(H-h)/2:enable='gte(t,5.5)'" \
-c:a copy out/shot_10_final.mp4
```

48 px a 55 % krytí. Pravidlo: **kdo to nehledá, nesmí to najít.** Jakmile je to
čitelné na první pohled, film přestal být otázkou a stal se odpovědí.

---

## Shrnutí

| Záběr | Riziko | Řešení |
|---|---|---|
| 7 | model nezná předchozí klipy | převinutí složit v ffmpegu z klipů 1–4 |
| 9 | nekonečno se rozpadne v kaši | 5 pojmenovaných světů + rozostřené okraje, nebo rozdělit na 9a/9b |
| 10 | detail buď zmizí, nebo rozhodne za diváka | vyhodit z promptu, dvojznačnost nese zvuk |

Společné pravidlo: **co model neumí udržet, nepatří do promptu — patří do střihu.**
