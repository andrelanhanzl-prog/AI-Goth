# Prompty pro Gemini

Nahraj `index.html` (Canvas nebo AI Studio) a použij jeden z těchto textů.

---

## 1. Základní zadání — vlož vždycky jako první

```
Tohle je moje osobní vizuální vyjádření: jsem dítě devadesátek, most mezi
starým a novým světem. Levá strana je kyberpunkové město (nový svět), pravá
strana je les a jezero (starý svět), uprostřed je táhlo — ten most.

Klíčová zásada, kterou nikdy neporušuj:
obsah je definovaný jen jednou v <template id="tpl"> a naklonovaný do obou
světů, takže musí mít v obou naprosto stejnou geometrii. Skiny (#cyber a
#nature) se smějí lišit jen barvou, stínem, pozadím a dekorací — nikdy ne
velikostí písma, řezem, rodinou písma, rozestupy ani rozměry. Jakmile se
metriky textu rozejdou, text se při přejezdu švem posune a most se rozbije.

Soubor musí zůstat jeden, bez externích knihoven, fontů a obrázků, aby fungoval
offline.

Uprav teď: ______
```

---

## 2. Hotové úpravy — dopiš na konec základního zadání

**Vlastní vzpomínky**
```
Vyměň dvojice v .pairs za tyhle moje vlastní a nech jich sedm:
<staré> → <nové>, ...
```

**Počítadlo let**
```
Přidej pod nadpis počítadlo, které při přejezdu mostu odpočítává rok od 1994
(úplně vlevo) do dneška (úplně vpravo). Ať se mění plynule podle proměnné --p
a je vysázené monospacem v obou světech stejně velké.
```

**Zvuk**
```
Přidej Web Audio API: vlevo tichý šum a pípání modemu, vpravo ptáci a vítr,
hlasitost se křížově míchá podle pozice mostu. Zvuk spusť až po prvním kliknutí
(autoplay policy) a dej do rohu tlačítko na ztlumení.
```

**Svislý most**
```
Otoč most na vodorovný: starý svět nahoře, nový dole, táhlo se posouvá svisle.
Uprav clip-path, šev, tažítko i ovládání klávesnicí (šipky nahoru/dolů).
```

**Fotka místo kreslených pozadí**
```
Nech mě vyměnit kreslená pozadí za moje dvě fotky: přidej input type="file"
na dva obrázky, ulož je do canvasu jako pozadí obou světů a zachovej ořez
i všechny efekty nad nimi.
```

**Sdílení**
```
Přidej tlačítko, které vyexportuje aktuální stav scény jako PNG přes
canvas.toDataURL — složí obě pozadí, částice i text do jednoho obrázku.
```

---

## 3. Když něco rozbije

```
Text na levé a pravé straně se při přejezdu posouvá. Najdi, kde se rozešly
metriky písma mezi #cyber a #nature, a vrať je na stejné hodnoty — lišit se
smí jen barva a stín.
```
