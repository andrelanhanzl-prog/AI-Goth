# KONEC CYKLU / THE CLOSING CYCLE

Materiál pro tvorbu ~64s filmu v Gemini (Veo). Téma: **dva cykly se uzavírají zároveň** —
tepelná smrt vesmíru a vyčerpání jedné civilizace. Oba dojdou do bodu, kde už nefunguje
setrvačnost a zbývá jen volba. Film se záměrně nerozhodne, kterou cestou se jde.

## Obsah

| Soubor | K čemu |
|---|---|
| `prompts/cyklus_do_gemini.md` | **8 hotových promptů k vložení do Gemini** — kopíruj blok po bloku |
| `prompts/cyklus_veo_prompt.json` | strukturovaný scénář (kamera, světlo, zvuk, negative prompt) |
| `scripts/generate_video.py` | vygeneruje všechny záběry přes API a slepí je do `out/film.mp4` |

## Ručně (bez API)

Otevři `prompts/cyklus_do_gemini.md`, vlož záběr 1 do Gemini, stáhni klip,
pokračuj záběrem 2 a tak dál. Na konec každého promptu přilep blok „Globální styl“.
Klipy pak slep v pořadí 1–8.

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
1–2  vesmír     entropie, chladnutí, konec bez katastrofy
3–4  společnost stejný tvar v jiném měřítku: spirála, vlna zhasínání, setrvačnost
5    ROZHRANÍ   jedna postava, dvě cesty, nikdo nerozhodl
6    větev A    popel — setrvačnost vyhrála
7    větev B    klíček — cyklus se otevřel znovu (nové hvězdy = obrácený záběr 2)
8    konec      návrat do záběru 5, bod světla nezhasne
```

Dva střihové zámky: **2→3** (spirála galaxie = spirála města) a **5→8** (identický
kompoziční záběr, jiný význam). V každém záběru je jeden kruhový zdroj světla —
hvězda, lampa, obrazovka, semínko, zornice. Napříč filmem se zmenšuje a na konci se
znovu otevře.
