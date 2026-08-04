# AI-Goth

Nástroj, který z textového **programu** (jeden YAML soubor) a zvukové stopy
vyrenderuje video. Obsah, časování i vzhled jsou v programu — v kódu není
zadrátovaná jediná věta. Chceš změnit sdělení, přepíšeš YAML, ne Python.

## Instalace

```bash
pip install -r requirements.txt
```

`ffmpeg` se bere systémový; když není, použije se binárka z `imageio-ffmpeg`
(je v `requirements.txt`, takže nic dalšího instalovat nemusíš).

## Použití

```bash
python -m aigoth validate projects/ukazka/program.yml   # kontrola bez renderu
python -m aigoth plan     projects/ukazka/program.yml   # časová osa scén
python -m aigoth preview  projects/ukazka/program.yml --at 40 -o snimek.png
python -m aigoth render   projects/ukazka/program.yml -o out/video.mp4
```

`plan` a `preview` jsou tu proto, aby se dalo ladit obsah a sazba bez čekání
na celý render.

## Program

```yaml
title: "Název"
resolution: [1920, 1080]   # šířka i výška musí být sudé (H.264)
fps: 30
audio: stopa.wav           # cesta relativně k tomuhle YAML

theme:
  background: "#08080b"    # základ pozadí
  foreground: "#e8e6e3"    # barva hlavního textu
  accent: "#8b1e2d"        # záře v pozadí a barva podtitulu
  font: null               # cesta k TTF; null = DejaVu Serif ze systému
  grain: 0.05              # filmové zrno, 0 = vypnuto
  vignette: 0.55           # ztmavení okrajů
  title_size: 0.075        # podíl výšky snímku
  subtitle_size: 0.032

scenes:
  - id: teze               # unikátní; objeví se ve výpisu `plan`
    duration: 9            # sekundy, nebo 'auto'
    text: "Hlavní řádek"   # zalomí se sám
    subtitle: "podtitul"
    background: gradient   # gradient | solid | image
    image: pozadi.jpg      # jen pro background: image (ořízne se na formát)
    align: center          # left | center | right
    fade: 1.2              # náběh a doběh v sekundách
    accent: "#c8b273"      # přebije theme.accent jen pro tuhle scénu
```

### Časování

Scény s číselnou `duration` mají pevnou délku. Scény s `duration: auto`
(nebo bez `duration`) si rovným dílem rozdělí čas, který ve stopě zbyde po
pevných scénách — takže se dá zafixovat intro a outro a zbytek nechat
dopočítat na délku hudby. Bez zvukové stopy dostane každá `auto` scéna 6 s.

Když délky nesedí na stopu, `validate` i `render` to napíšou jako varování,
ale render proběhne.

## Poznámky k renderu

- Zrno je nepřítel komprese: `grain: 0.05` nafoukne soubor i několikrát.
  Na menší výstup dej `grain: 0` nebo zvyš `--crf` (výchozí 18, vyšší =
  menší soubor a horší obraz).
- Render je deterministický — i zrno je odvozené od čísla snímku, takže
  dvakrát spuštěný render dá bit po bitu stejné video.
- Rychlost se ladí přes `--preset` (`ultrafast` … `veryslow`).

## Testy

```bash
python -m pytest tests -q
```
