# KONEC CYKLU / THE CLOSING CYCLE

Materiál pro tvorbu ~80s filmu v Gemini (Veo). Téma: **dva cykly se uzavírají zároveň** —
tepelná smrt vesmíru a vyčerpání jedné civilizace. Oba dojdou do bodu, kde už nefunguje
setrvačnost a zbývá jen volba mezi dvěma geometriemi:

- **robotika = uzavřená smyčka** → systém se restartuje, všechno proběhne znovu identicky
- **svoboda = větvení** → jeden svět se roztrhne na multivesmír, kde se stane všechno možné

Film se záměrně nerozhodne, kterou cestou se jde.

## Obsah

| Soubor | K čemu |
|---|---|
| `prompts/cyklus_do_gemini.md` | **10 hotových promptů k vložení do Gemini** — kopíruj blok po bloku |
| `prompts/cyklus_veo_prompt.json` | strukturovaný scénář (kamera, světlo, zvuk, negative prompt) |
| `scripts/generate_video.py` | vygeneruje všechny záběry přes API a slepí je do `out/film.mp4` |

## Ručně (bez API)

Otevři `prompts/cyklus_do_gemini.md`, vlož záběr 1 do Gemini, stáhni klip,
pokračuj záběrem 2 a tak dál. Na konec každého promptu přilep blok „Globální styl“
(výjimka: záběr 9, kde se paleta záměrně trhá do plného spektra).
Klipy pak slep v pořadí 1–10.

## Přes API

```bash
pip install google-genai
export GEMINI_API_KEY=...
python scripts/generate_video.py --seed 42 --chain --ffmpeg
```

- `--seed` drží vizuální konzistenci mezi záběry
- `--chain` posílá poslední snímek předchozího klipu jako vstup dalšího (plynulejší návaznost)
- `--ffmpeg` slepí výsledek do `out/film.mp4`
- model se přepíná přes `VEO_MODEL` (default `veo-3.1-generate-preview`)

## Stavba

```
1–2   vesmír      entropie, chladnutí, konec bez katastrofy
3–4   společnost  stejný tvar v jiném měřítku: spirála, vlna zhasínání, setrvačnost
5     ROZHRANÍ    jedna postava, vlevo smyčka, vpravo větvení, nikdo nerozhodl
6–7   robotika    dokonalý řád → uzavřený kruh → restart, všechno znovu identicky
8–9   svoboda     jedna čára praskne → multivesmír, každý svět jiný, nic se neopakuje
10    konec       návrat do záběru 5, bod světla nezhasne
```

Tři střihové zámky: **2→3** (spirála galaxie = spirála města), **7→1** (restart
doslova vrací do prvního záběru) a **5→10** (identický kompoziční záběr, jiný význam).

**Geometrické pravidlo, které nese celý význam:** větev A je kruh — mřížka, opakování,
všechno zapadá na místo. Větev B je strom — rozdvojení, fraktál, nic dvakrát stejně.

Větev A není zkáza, je to dokonalé zachování bez východu. Větev B není spása, je to
neomezená možnost bez záruky. Hrůza i naděje jsou v obou.

V každém záběru je jeden kruhový zdroj světla — hvězda, lampa, obrazovka, zornice.
Napříč filmem se zmenšuje: ve větvi A se uzavře do dokonalého prstence, ve větvi B se
roztříští na nespočet bodů, v posledním záběru je jeden bod, který drží obojí.
