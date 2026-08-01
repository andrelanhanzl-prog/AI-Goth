Hotovo. Máš tři soubory:

- **`GEMINI_PASTE.json`** — pracovní soubor. Šest promptů, každý kompletní, nic se
  před ně ani za ně nepřidává.
- **`ZIMNI_NABIDKA_shoty.md`** — to samé pro člověka: co který záběr dělá,
  střihový plán, co Veo neumí a jak to obejít.
- **`scenario.json`** — zdroj, ze kterého se JSON staví. Když budeš chtít změnit
  paletu nebo styl, měníš to na jednom místě a přegeneruješ.

**Jak to funguje:** Veo dělá klipy po ~8 vteřinách a nepamatuje si nic z toho, co
vygenerovalo předtím. Třicetivteřinové video proto není jeden prompt, ale šest
generování plus střih. Generuješ 6×8 s = 48 s a stříháš na 30 — máš z čeho vybírat
a rezervu, když se jeden klip nepovede.

**Prompty jsou anglicky schválně.** Tyhle modely jsou trénované skoro výhradně na
anglických popiscích a v češtině znatelně ztrácejí. Do reklamy stejně půjde text
až ve střihu.

**Proč to bude vypadat dráž, než to je** — celý balíček stojí na jednom
rozhodnutí: *kavárnu nikdy neukážeme.* Pět ze šesti záběrů je makro na sklo,
tekutinu, páru a ruce. Jeden zdroj světla, žádné doplňkové, pozadí padá do
černé, malá hloubka ostrosti, všechno pomalu. Plošné stropní světlo a ostrý
interiér jsou vizuální podpis levné reklamy; tma je zadarmo a co není vidět,
nemusí být hezké.

**Co drží klipy pohromadě:** v každém jednom záběru je jedna teplá jantarová
lampa a jedno studené modré okno. Mění se jen jejich poměr — 90/10 ve prospěch
studené v prvním záběru, 85/15 ve prospěch teplé v posledním. To je zároveň
hodiny celého spotu, divák bez přemýšlení cítí, že se někam došlo. Když budeš
záběr přegenerovávat, ten poměr v promptu nech tak, jak je.

Jedna věc, kterou neopravuj: **vínová barva je v prvním záběru zakázaná
schválně** a poprvé se objeví až u nálevu ve druhém. Je to jediný moment, kdy se
film barevně „zapne".

**Tři věci, které Veo neumí — ať to nezjistíš až u generování:**

1. **Text, cena, název, logo.** Čeština s diakritikou vyleze jako patvar, logo
   nepřenese vůbec. Všechna slova jdou ve střihu na poslední záběr, který je
   proto naframovaný s prázdnou horní třetinou.
2. **Ruce (záběr 5).** Pořád slabina těchhle modelů, počítej se třemi pokusy.
   V `.md` máš zjednodušenou variantu s nehybnýma rukama — tu model zvládne
   skoro vždycky a ve čtyřech vteřinách funguje stejně.
3. **Nebude to vaše kavárna.** Je to náladové video k vaší nabídce, ne dokument o
   vašem podniku, a když se to prodává jako „u nás", je to na hraně. Nejlepší
   řešení je levné: natoč mobilem dva reálné záběry — váš hrnek, váš pult — a
   dej je do střihu místo záběrů 3 a 5. Reálný detail a generovanou atmosféru
   od sebe nikdo nerozezná a reklama přestane lhát. Případně vyfoť svůj hrnek na
   tmavém pozadí a pusť ho do Veo jako vstupní obrázek pro image-to-video.

**Praktické:** v Gemini přepni formát na 9:16, vlož celý JSON a piš
`Generate shot 1.`, `Generate shot 2.` — po jednom. Seed drž po celou sadu
stejný. Zvuk si Veo vygeneruje, ale Instagram se z většiny kouká bez zvuku —
ambient používej jako texturu pod jednu licencovanou skladbu přes celých 30 s.
A úplně na konec pusť přes všech šest klipů jeden společný barevný průchod;
ffmpeg příkaz máš v `.md`. To je nejrychlejší způsob, jak z nezávisle
vygenerovaných záběrů udělat jeden film — často účinnější než cokoliv v promptech.
