/* AI-Goth :: Fiery Angel — složení scény */
window.AG = window.AG || {};

(function (AG) {
  'use strict';
  const U = AG.U, LY = AG.layers;

  /* Výchozí nastavení šablony. Vše je přepsatelné z panelu vpravo. */
  const DEFAULTS = {
    palette: 'lucifer',
    format: '9:16',
    duration: 15,          // délka smyčky v sekundách
    title: 'LUCIFER',
    subtitle: 'světlonoš',
    titleY: 0.30,          // pozice titulku ode dna (v jednotkách S)
    textAlign: 'left',     // left | center | right
    asym: 0.6,             // rozvážení celé kompozice mimo osu
    font: '"Arial Black", "Helvetica Neue", Impact, sans-serif',

    intensity: 0.85,       // celková síla ohně
    wingSize: 1.0,
    halo: true,
    smoke: 0.9,
    emberAmount: 1.0,
    emberSpeed: 1.0,
    heat: 0.5,             // vlnění horkého vzduchu přes portrét
    duotone: 0.8,          // síla ohnivé gradace fotky
    contrast: 0.5,
    vignette: 0.6,
    grain: 0.35,

    photoScale: 1.0,
    photoX: 0,
    photoY: 0,
    photoRotate: 0,
    photoFraming: 0.0,     // posun výřezu uvnitř rámu
    mask: 'oval',          // oval | burn | none
    focus: 1.0,            // jak těsně se maska stahuje kolem obličeje
    focusX: 0,             // střed masky a světla — nastav na obličej
    focusY: 0,
    haloY: 0.04,           // výška svatozáře v rámci portrétu
    bodyShadow: 0.7,       // temná hmota ramen pod portrétem
  };

  const FORMATS = {
    '9:16': [1080, 1920],
    '1:1': [1080, 1080],
    '16:9': [1920, 1080],
    '4:5': [1080, 1350],
  };

  const embers = LY.makeEmbers(190);

  function layout(W, H, cfg) {
    const S = Math.min(W, H);
    const a = cfg ? cfg.asym : 0;
    return {
      W, H, S,
      // postava je záměrně mimo osu — asymetrie drží kompozici při životě
      cx: W * (0.5 - 0.06 * a),
      cy: H * (H > W ? 0.44 : 0.46) - S * 0.02 * a,
      portraitW: S * 0.52,
      wingLen: Math.min(W * 0.44, S * 0.52),
    };
  }

  /* Vykreslí jeden snímek v čase t (sekundy) na daný kontext. */
  function render(ctx, cfg, image, t) {
    const dim = FORMATS[cfg.format] || FORMATS['9:16'];
    const W = dim[0], H = dim[1];
    const L = layout(W, H, cfg);
    const P = AG.PALETTES[cfg.palette] || AG.PALETTES.lucifer;
    const dir = AG.direct(t % cfg.duration, cfg.duration);
    const s = { cfg, image, dir };

    ctx.save();
    ctx.globalCompositeOperation = 'source-over';
    ctx.clearRect(0, 0, W, H);

    LY.drawBackground(ctx, L, P, s);
    LY.drawEmbers(ctx, L, P, s, embers, false);   // uhlíky za postavou
    LY.drawWings(ctx, L, P, s);
    LY.drawPortrait(ctx, L, P, s);
    LY.drawHalo(ctx, L, P, s);
    LY.drawFlames(ctx, L, P, s);
    LY.drawEmbers(ctx, L, P, s, embers, true);    // uhlíky před postavou
    LY.drawText(ctx, L, P, s);
    LY.drawGrade(ctx, L, P, s);

    ctx.restore();
    return { W, H };
  }

  AG.scene = { DEFAULTS, FORMATS, render, layout };
})(window.AG);
