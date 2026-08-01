# Zimní nabídka — 30s vertikální spot pro Instagram

Balíček pro Veo (přes Gemini). Šest klipů po 8 s, sestříhaných na 30 s.
Prompty jsou **anglicky schválně** — Veo je trénované hlavně na anglických
popiscích a v češtině znatelně ztrácí. Text v reklamě bude stejně až ve střihu.

Prompty k vkládání jsou v `GEMINI_PASTE.json`. Tenhle soubor je na režii —
abys věděl, co kterej záběr dělá, až budeš něco přegenerovávat.

---

## Páteř

**Venku je zima a modro, tady uvnitř je jantar a teplo.** Nic víc se neděje a nic
víc se dít nemusí. Na konci je hrnek plnej a okno zamlžený; na začátku bylo sklo
studený a na druhý straně nic.

## Proč to bude vypadat dráž, než to je

Celý to stojí na jednom rozhodnutí: **kavárnu nikdy neukážeme.** Pět ze šesti
záběrů je makro na sklo, tekutinu, páru a ruce, šestý je pomalý odjezd, kde je
ostrý jenom hrnek a všechno ostatní se rozplývá do tmy.

Drahý to dělá tohle, ne rozpočet:

- **Jeden zdroj světla a žádné doplňkové.** Pozadí padá do skoro černé. Plošné
  stropní světlo je vizuální podpis levné reklamy.
- **Malá hloubka ostrosti.** Nejúčinnější jediná věc, která odliší
  „vyfoceno" od „vygenerováno".
- **Pomalu.** Rychlý pohyb je přesně místo, kde se AI video rozsype — a pomalá
  jízda navíc čte jako dražší.
- **Tma.** Co není vidět, to nemusí být hezké.

## Kotva konzistence

Klipy o sobě navzájem nevědí. Jediné, co je slepí dohromady, je věc, kterou
popíšeš stejně v každém promptu:

> **Jedna teplá jantarová lampa + jedno studené břidlicově modré okno, v každém
> jednom záběru.** Mění se jen jejich poměr.

| Záběr | Poměr studená / teplá |
|---|---|
| 1 Okno | 90 / 10 |
| 2 Nálev | 40 / 60 |
| 3 Koření | 30 / 70 |
| 4 Pára | 20 / 80 |
| 5 Ruce | 20 / 80 |
| 6 Stůl u okna | 15 / 85 |

Tenhle poměr je zároveň hodiny celého spotu — divák bez přemýšlení cítí, že se
někam došlo. Když budeš záběr přegenerovávat, **poměr v promptu nech tak, jak je.**

**Vínová je v záběru 1 zakázaná schválně.** Poprvé se objeví až v záběru 2 s
nálevem. Neopravuj to — je to jediný barevný moment, kdy se film „zapne".

## Paleta

`deep espresso brown, mulled-wine burgundy, amber candlelight, cold slate blue, bone white`

Ve všech šesti promptech je totožná. Rozjetá paleta je nejviditelnější známka
toho, že video vzniklo po klipech.

---

## Střihový plán

| # | Záběr | Práce ve filmu | Generuj | Ve střihu |
|---|---|---|---|---|
| 1 | Okno | expozice — zima | 8 s | 4 s |
| 2 | Nálev | produkt přichází | 8 s | 5 s |
| 3 | Koření | textura, důvod ceny | 8 s | 4 s |
| 4 | Pára | textura, dech | 8 s | 5 s |
| 5 | Ruce | obrat — je to tvoje | 8 s | 5 s |
| 6 | Stůl u okna | pointa + místo na text | 8 s | 7 s |
| | | | 48 s | **30 s** |

Generuješ víc, než použiješ, schválně — vybereš si nejlepších pět vteřin z osmi a
máš rezervu, když se jeden klip nepovede.

**Střihy na tvar (match cuty):** záběr 1 končí na kulaté svatozáři lampy, záběr 2
začíná na kulatém okraji hrnku. Záběr 3 končí na kulaté pomerančové kůře, záběr 4
začíná na kulatém kotouči lampy. Oko takový střih přijme jako záměr, ne jako
sklížení dvou cizích klipů.

**Rým:** záběr 1 a záběr 6 se dívají na stejné okno — první ze studené strany,
poslední z teplé.

---

## Záběry

Každý prompt je kompletní. Nic se před něj ani za něj nepřidává.

### 1 — Okno

Studený start. Vínová tu ještě není. Jediné teplo je rozostřená koule světla za
sklem — slib, ne odměna.

```
Extreme close macro of frost crystals and condensation on the inside of a cafe window at blue winter dusk. One single drop of condensation slides slowly down the cold glass. Far behind the glass, heavily out of focus, a warm amber lamp burns as one soft round halo of light. Camera: slow push-in, 85mm macro, locked horizon, no movement other than the push, vertical 9:16 framing. Lighting: cold slate-blue dusk light through the window as the only key, one small warm amber practical far in the background as the single warm source, roughly ninety percent cold to ten percent warm, the lower third of the frame falling into deep shadow. Style: shot on 35mm film, shallow depth of field, fine natural grain, gentle halation on the warm highlights, vertical 9:16 framing, slow deliberate motion, photographed not rendered. Palette: deep espresso brown, mulled-wine burgundy, amber candlelight, cold slate blue, bone white. Audio: muffled winter street outside the glass, a faint low interior room hum, one sustained warm synth pad held under everything. No dialogue. Avoid: text, subtitles, captions, watermarks, logos, brand labels, packaging, interface elements, fast cuts, camera shake, handheld jitter, flat overhead fluorescent light, oversaturated colours, plastic cups, cluttered background, people, faces, any red or burgundy anywhere in frame, the cafe interior in sharp focus, direct view of the lamp bulb.
```

### 2 — Nálev

Jediná událost: nálev. Zpomaleně, protože zpomalené tekutině Veo věří a vypadá
to draho. V zákazech je `splashing, spilling` — cákance jsou tady typická chyba.

```
Dark mulled wine pours in one slow steady stream from a battered copper pan into a heavy footed glass mug standing on a dark oiled wood counter, steam curling off the rising surface as the mug fills. Slow motion, 60fps feel. Camera: static locked-off medium close, 50mm, framed on the mug with the pan entering from the top of the frame, shallow depth of field, vertical 9:16 framing. Lighting: single warm amber practical just out of frame camera left, no fill, the background falling to near black, one thin cold slate-blue rim from a window far camera right, roughly sixty percent warm to forty percent cold. Style: shot on 35mm film, shallow depth of field, fine natural grain, gentle halation on the warm highlights, vertical 9:16 framing, slow deliberate motion, photographed not rendered. Palette: deep espresso brown, mulled-wine burgundy, amber candlelight, cold slate blue, bone white. Audio: the low pour of hot liquid into thick glass, quiet crackle of a room in winter, the same sustained warm synth pad continuing. No dialogue. Avoid: text, subtitles, captions, watermarks, logos, brand labels, packaging, interface elements, fast cuts, camera shake, handheld jitter, flat overhead fluorescent light, oversaturated colours, plastic cups, cluttered background, splashing, spilling, overflowing, hands, faces, steel or plastic vessels.
```

### 3 — Koření

Skořice, badyán, pomerančová kůra. Pohybuje se jen kůra — jedna věc na záběr.
Světlo jde nízko zboku, aby se pára chytila.

```
Extreme macro on the dark surface of mulled wine inside a glass mug: a cinnamon stick, one star anise and a curl of orange peel float on the liquid, and the orange peel turns slowly in place as thin steam rises past the lens. Camera: extreme macro, 100mm, very slow push-in over the rim of the mug, shallow depth of field with the far rim already soft, vertical 9:16 framing. Lighting: warm amber practical low from camera left raking across the liquid surface so the steam catches the light, deep shadow beyond the rim, a faint cold slate-blue reflection on the far side of the glass, roughly seventy percent warm to thirty percent cold. Style: shot on 35mm film, shallow depth of field, fine natural grain, gentle halation on the warm highlights, vertical 9:16 framing, slow deliberate motion, photographed not rendered. Palette: deep espresso brown, mulled-wine burgundy, amber candlelight, cold slate blue, bone white. Audio: close quiet liquid settling, a distant espresso machine two rooms away, the warm synth pad with one soft low piano note added. No dialogue. Avoid: text, subtitles, captions, watermarks, logos, brand labels, packaging, interface elements, fast cuts, camera shake, handheld jitter, flat overhead fluorescent light, oversaturated colours, plastic cups, cluttered background, hands, spoons, stirring, faces, scattered spices outside the mug.
```

### 4 — Pára

Nejlevnější a nejúčinnější záběr celého spotu. Protisvětlo skrz páru dělá půlku
práce, kterou by jinak dělal rozpočet.

```
A thick slow ribbon of steam rises off the surface of dark red mulled wine and drifts across the amber lamp burning behind it, glowing bright as it passes through the light and vanishing into the dark above. Camera: static locked-off close, 85mm, the mug low and slightly left of centre, the lamp a soft blown-out disc behind the steam, shallow depth of field, vertical 9:16 framing. Lighting: the amber practical sits directly behind the steam as a hard backlight so the steam edges glow, no fill at all, everything outside the steam near black, one cold slate-blue sliver at the extreme frame edge, roughly eighty percent warm to twenty percent cold. Style: shot on 35mm film, shallow depth of field, fine natural grain, gentle halation on the warm highlights, vertical 9:16 framing, slow deliberate motion, photographed not rendered. Palette: deep espresso brown, mulled-wine burgundy, amber candlelight, cold slate blue, bone white. Audio: near silence, a slow ticking clock, the warm synth pad swelling very slightly. No dialogue. Avoid: text, subtitles, captions, watermarks, logos, brand labels, packaging, interface elements, fast cuts, camera shake, handheld jitter, flat overhead fluorescent light, oversaturated colours, plastic cups, cluttered background, smoke that looks like fog machine haze, fire, sparks, hands, faces.
```

### 5 — Ruce

Nejrizikovější záběr — ruce jsou pořád slabina těchhle modelů. Proto jsou v
záběru jen dlaně a rukáv, žádná manipulace s ničím, a v zákazech je celý seznam
prstových katastrof. **Počítej s tím, že tenhle budeš generovat třikrát.**
Když to nepůjde, alternativa je níž.

```
Two hands wrap around the warm glass mug and lift it slowly off the wooden counter towards the top of the frame. Only the hands, the sleeves of a thick charcoal wool sweater and the mug are visible. Camera: slow push-in, 50mm, framed from the wrists down to the counter surface, the face never in frame, shallow depth of field, vertical 9:16 framing. Lighting: warm amber practical from camera left as the key with a soft falloff across the knuckles, deep shadow on the right side of the hands, thin cold slate-blue edge light on the far side of the glass, roughly eighty percent warm to twenty percent cold. Style: shot on 35mm film, shallow depth of field, fine natural grain, gentle halation on the warm highlights, vertical 9:16 framing, slow deliberate motion, photographed not rendered. Palette: deep espresso brown, mulled-wine burgundy, amber candlelight, cold slate blue, bone white. Audio: the small sound of glass leaving a wooden surface, a low winter room tone, the warm synth pad with a single sustained cello note underneath. No dialogue. Avoid: text, subtitles, captions, watermarks, logos, brand labels, packaging, interface elements, fast cuts, camera shake, handheld jitter, flat overhead fluorescent light, oversaturated colours, plastic cups, cluttered background, distorted hands, extra fingers, fused fingers, six fingers, rings, jewellery, wristwatch, long fingernails, faces, arms in unnatural poses.
```

### 6 — Stůl u okna

Pointa a jediný záběr, kde je vidět kus prostoru. Horní třetina je schválně
prázdná zeď — tam přijde ve střihu název, nabídka a cena.

```
The full glass mug of mulled wine steams gently on a small dark wooden table beside the fogged cafe window. Beyond the glass, snow falls slowly through the blue evening. The upper third of the frame stays empty dark wall. Camera: slow continuous pull-back from close to medium wide, 35mm, locked horizon, ending with the mug low in the lower third and clean empty space above it, vertical 9:16 framing. Lighting: the warm amber practical now the dominant key from camera left filling the room, the cold slate-blue window light reduced to a thin rim on the glass and on the falling snow, roughly eighty-five percent warm to fifteen percent cold. Style: shot on 35mm film, shallow depth of field, fine natural grain, gentle halation on the warm highlights, vertical 9:16 framing, slow deliberate motion, photographed not rendered. Palette: deep espresso brown, mulled-wine burgundy, amber candlelight, cold slate blue, bone white. Audio: quiet cafe room tone, a spoon somewhere off frame, snow-muffled street, the warm synth pad and cello resolving to one held chord. No dialogue. Avoid: text, subtitles, captions, watermarks, logos, brand labels, packaging, interface elements, fast cuts, camera shake, handheld jitter, flat overhead fluorescent light, oversaturated colours, plastic cups, cluttered background, people, faces, chairs pulled out, menus, signage, a busy or cluttered room, anything in sharp focus behind the window.
```

---

## Co Veo neumí — řekni si to teď, ne až u generování

### Text, název, cena, logo

**Neumí.** Čitelný text a hlavně čeština s diakritikou vyleze jako patvar, logo
nepřenese vůbec. Ani se o to nepokoušej promptem — proto je ve všech zákazech
`text, logos, brand labels`.

*Řešení:* všechna slova jdou ve střihu na záběr 6, kde je nahoře prázdná zeď.
Jedna sazba, dva řádky, nic víc. Text nad obrazem navíc vždycky vypadá dráž než
text vygenerovaný v obraze.

### Váš skutečný hrnek / váš skutečný interiér

**Tohle nebude vaše kavárna.** Je to náladové video k vaší nabídce, ne dokument o
vašem podniku. Když se to prodává jako „u nás", je to na hraně.

*Řešení A (poctivé a nejlepší):* natoč mobilem dva reálné záběry — váš hrnek, váš
pult — a dej je do střihu na místa 3 a 5. Zbytek nechá AI. Mix reálného detailu a
generované atmosféry je vizuálně nerozeznatelný a reklama přestane lhát.

*Řešení B:* vyfoť svůj hrnek na tmavém pozadí a použij ten snímek jako vstupní
obrázek pro image-to-video. Veo z něj vyjde a hrnek zůstane váš.

### Stejný hrnek ve všech šesti záběrech

Nebude přesně stejný. Modely si mezi klipy nic nepamatují.

*Řešení:* proto je pět ze šesti záběrů makro — na detailu se drobná neshoda tvaru
neprozradí. Kde ti to bude vadit (typicky přechod 4 → 5 → 6), vyexportuj poslední
snímek klipu a pusť ho do dalšího jako vstupní obrázek:

```bash
ffmpeg -y -sseof -0.1 -i shot_04.mp4 -frames:v 1 shot_04_last.png
```

To je nejsilnější nástroj na návaznost, jaký máš, a stojí nula.

### Ruce (záběr 5)

Nejčastější místo, kde to praskne — prsty navíc, srostlé klouby.

*Zjednodušená varianta, když se to nedaří:* vynech zvedání a nech ruce jen ležet
kolem hrnku. Nahraď první větu promptu 5 tímhle a zbytek nech beze změny:

```
Two still hands rest wrapped around a warm glass mug on a dark wooden counter, completely motionless, only the steam moving. Only the hands, the sleeves of a thick charcoal wool sweater and the mug are visible.
```

Nehybné ruce zvládne model skoro vždycky. A ve 4sekundovém záběru to funguje
stejně dobře.

### Zvuk

Veo zvuk vygeneruje, ale **Instagram se z 80 % kouká bez zvuku.** Generovaný
ambient používej jako texturu pod hudbu, ne jako hlavní stopu — do střihu dej
jednu licencovanou skladbu přes celých 30 s. `No dialogue` je v každém promptu
schválně, jinak si model vymyslí zamumlanou větu.

---

## Jak to prakticky odjet

1. Otevři Gemini, nahoď Veo, přepni formát na **9:16**.
2. Vlož celý `GEMINI_PASTE.json` a napiš `Generate shot 1.` Pak `Generate shot 2.`
   a tak dál. Nebo prostě zkopíruj jednu hodnotu `paste` samostatně — každá je
   kompletní a nic se k ní nepřidává.
3. **Seed drž po celou sadu stejný.** Když jeden klip vyjde teplejší nebo světlejší,
   srovnej to v barvách, nepřegenerovávej.
4. Ze šesti klipů vyber nejlepší úsek podle střihového plánu výš.
5. Text a logo až úplně nakonec, na záběr 6.

### Bezpečné zóny Instagramu

Reels ti překryjí spodních zhruba 250 px (popisek, tlačítka) a horních 120 px.
Proto má záběr 6 hrnek dole a prázdno nahoře — ale **text posaď do prostřední
třetiny**, ne úplně nahoru a rozhodně ne dolů.

### Slepení a barevné sjednocení

```bash
# ořezy podle střihového plánu
ffmpeg -y -i shot_01.mp4 -ss 2 -t 4 -c:v libx264 -crf 18 c1.mp4
ffmpeg -y -i shot_02.mp4 -ss 1 -t 5 -c:v libx264 -crf 18 c2.mp4
# ... a tak dál

printf "file 'c%d.mp4'\n" $(seq 1 6) > concat.txt
ffmpeg -y -f concat -safe 0 -i concat.txt -c copy spot.mp4
```

Jeden společný barevný průchod přes všech šest klipů nakonec je nejrychlejší
způsob, jak z nezávisle vygenerovaných záběrů udělat jeden film — často účinnější
než cokoliv v promptech:

```bash
ffmpeg -y -i spot.mp4 -vf "eq=saturation=0.92:contrast=1.06:gamma=0.97, \
colorbalance=rs=0.03:bs=-0.03" -c:a copy spot_graded.mp4
```

Mírně snížená sytost a lehce zvednutý kontrast — to je celý ten „drahý" look.
