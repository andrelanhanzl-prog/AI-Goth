# 🔥 Ohnivý anděl — šablona pro video

Animovaná šablona, která z běžné fotky udělá padlého anděla v plamenech.
Všechno běží v prohlížeči na `<canvas>` — žádná instalace, žádný build,
žádné odesílání fotky na server. Výsledek se dá uložit jako **video (WebM)**
nebo jako **snímek (PNG)**.

![formáty 9:16, 4:5, 1:1 a 16:9](#)

## Spuštění

Otevři `index.html` v prohlížeči (dvojklik stačí). Doporučený je Chrome nebo
Edge — jen ty umí spolehlivě nahrát plátno do videa.

Případně přes lokální server:

```bash
python3 -m http.server 8000    # pak otevři http://localhost:8000
```

## Jak z toho udělat video

1. **Vlož fotku** — tlačítkem v panelu, nebo ji prostě přetáhni na náhled.
2. **Srovnej ji** — `Otočit o 90°` (fotky z mobilu bývají na bok), pak
   posun, velikost a *Střed ↔ / ↕*, aby maska seděla na obličej.
3. **Vyber předvolbu** — Lucifer, Inferno, Serafín, Propast, Popel.
4. **Napiš text** — titulek a podtitul, včetně výšky a zarovnání.
5. **Zvol formát** — 9:16 pro Reels a TikTok, 16:9 pro YouTube, 1:1 a 4:5 pro feed.
6. **⏺ Nahrát video** — nahraje přesně jednu smyčku a stáhne `.webm`.

Převod na MP4, když ho platforma vyžaduje:

```bash
ffmpeg -i ai-goth-ohnivy-andel.webm -c:v libx264 -pix_fmt yuv420p -crf 18 video.mp4
```

## Co scéna obsahuje

| Vrstva | Co dělá |
| --- | --- |
| Pozadí | temná obloha, stoupající kouř, doutnající obzor |
| Křídla | procedurální ohnivá pera na dvou křivkách, rozevírají se a plápolají |
| Portrét | duotónová gradace do barev ohně, měkká maska, obrysové světlo, vlnění žáru |
| Svatozář | nakřivo zavěšený prstenec s obíhajícími jiskrami |
| Oheň | uhlíky před i za postavou, plamenné šlehy u spodní hrany |
| Text | titulek, který se „vypaluje“ odspodu nahoru |
| Gradace | vinětace, filmové zrno, náběh a doběh do černé |

### Časová osa

Klip je stavěný jako smyčka (výchozí 15 s): tma → žár → portrét → rozevření
křídel → svatozář → vypálení titulku → podtitul → ztmavení zpět do černé.
Režii má na starost `AG.direct()` v `js/core.js`; posunutím čísel se dá celý
rytmus přestavět.

### Asymetrie

Posuvník **Asymetrie** rozváží celou kompozici mimo osu: křídla dostanou
jinou velikost, náklon i výšku, postava se posune ze středu, oheň hoří
silněji na jedné straně, uhlíky letí šikmo, svatozář visí nakřivo a text se
kotví ke straně. Na nule je obraz souměrný jako logo — což bývá to poslední,
co člověk od zjevení v plamenech chce.

## Struktura

```
index.html      rozhraní a ovládací panel
css/style.css   vzhled panelu
js/core.js      matematika, šum, barevné palety, časová osa
js/layers.js    vykreslení jednotlivých vrstev
js/scene.js     výchozí nastavení, formáty, složení snímku
js/app.js       ovládání, přehrávání, export snímku a videa
```

## Programové ovládání

Šablona vystavuje jednoduché API — hodí se na dávkové generování variant
nebo na ladění v konzoli prohlížeče:

```js
await AG.api.setImage('data:image/jpeg;base64,…');
AG.api.set({ title: 'SAMAEL', palette: 'abyss', asym: 0.9 });
AG.api.seek(6.5);              // skok na konkrétní čas
AG.api.canvas.toDataURL();     // hotový snímek
```

Všechna nastavení jsou v `AG.scene.DEFAULTS` v `js/scene.js`.

## Poznámky

- Fotka se nikam neodesílá, zpracovává se celá v prohlížeči.
- Nahrávání videa potřebuje `MediaRecorder` a `canvas.captureStream()`.
  Pokud je prohlížeč nemá, zbývá záznam okna přes OBS.
- Efekty jsou deterministické — stejné nastavení dá pokaždé stejný snímek.
