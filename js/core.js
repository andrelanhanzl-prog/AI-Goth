/* AI-Goth :: Fiery Angel — jádro (pomocné funkce, šum, palety, časová osa) */
window.AG = window.AG || {};

(function (AG) {
  'use strict';

  /* ---------- matematika ---------- */
  const U = {
    clamp: (v, a, b) => (v < a ? a : v > b ? b : v),
    lerp: (a, b, t) => a + (b - a) * t,
    mix: (a, b, t) => a + (b - a) * t,
    smoothstep(e0, e1, x) {
      const t = U.clamp((x - e0) / (e1 - e0 || 1e-6), 0, 1);
      return t * t * (3 - 2 * t);
    },
    easeOutCubic: (t) => 1 - Math.pow(1 - t, 3),
    easeOutBack(t) {
      const c1 = 1.70158, c3 = c1 + 1;
      return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2);
    },
    easeInOut: (t) => (t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2),
    /* deterministický "náhodný" generátor — aby byl každý běh stejný a video se dalo zopakovat */
    hash(n) {
      const s = Math.sin(n * 127.1 + 311.7) * 43758.5453;
      return s - Math.floor(s);
    },
    hash2(x, y) {
      const s = Math.sin(x * 127.1 + y * 311.7) * 43758.5453;
      return s - Math.floor(s);
    },
  };

  /* plynulý 1D šum — pro plápolání a vlnění */
  U.noise1 = function (x) {
    const i = Math.floor(x), f = x - i;
    const u = f * f * (3 - 2 * f);
    return U.mix(U.hash(i), U.hash(i + 1), u);
  };

  /* 2D value noise — kouř, žár */
  U.noise2 = function (x, y) {
    const ix = Math.floor(x), iy = Math.floor(y);
    const fx = x - ix, fy = y - iy;
    const ux = fx * fx * (3 - 2 * fx), uy = fy * fy * (3 - 2 * fy);
    const a = U.hash2(ix, iy), b = U.hash2(ix + 1, iy);
    const c = U.hash2(ix, iy + 1), d = U.hash2(ix + 1, iy + 1);
    return U.mix(U.mix(a, b, ux), U.mix(c, d, ux), uy);
  };

  U.fbm = function (x, y, oct) {
    let v = 0, amp = 0.5, fx = x, fy = y;
    for (let i = 0; i < (oct || 4); i++) {
      v += amp * U.noise2(fx, fy);
      fx *= 2.02; fy *= 2.02; amp *= 0.5;
    }
    return v;
  };

  U.rgba = function (rgb, a) {
    return 'rgba(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ',' + a + ')';
  };

  /* ---------- barevné palety ---------- */
  const PALETTES = {
    lucifer: {
      name: 'Lucifer (rudo-zlatá)',
      core: [255, 246, 214],   // nejžhavější jádro
      hot: [255, 186, 66],     // zlatý plamen
      mid: [232, 84, 26],      // oranžová
      deep: [124, 16, 12],     // temně rudá
      smoke: [38, 14, 16],     // kouř / pozadí
      sky: [12, 5, 8],         // nejtmavší bod pozadí
      rim: [255, 150, 60],     // obrysové světlo na obličeji
      shadow: [26, 8, 12],     // stíny duotonu
    },
    hellfire: {
      name: 'Pekelný oheň',
      core: [255, 252, 232],
      hot: [255, 140, 24],
      mid: [214, 44, 12],
      deep: [92, 8, 6],
      smoke: [30, 12, 10],
      sky: [8, 4, 4],
      rim: [255, 110, 40],
      shadow: [20, 6, 6],
    },
    abyss: {
      name: 'Modrá propast',
      core: [236, 250, 255],
      hot: [120, 200, 255],
      mid: [56, 108, 232],
      deep: [22, 26, 112],
      smoke: [10, 14, 34],
      sky: [4, 5, 14],
      rim: [140, 200, 255],
      shadow: [8, 10, 26],
    },
    wraith: {
      name: 'Jedovatě zelená',
      core: [240, 255, 226],
      hot: [166, 255, 96],
      mid: [56, 190, 72],
      deep: [12, 78, 40],
      smoke: [10, 24, 16],
      sky: [4, 9, 7],
      rim: [150, 255, 120],
      shadow: [8, 18, 12],
    },
    ash: {
      name: 'Popelavá (černobílá)',
      core: [255, 255, 255],
      hot: [226, 226, 226],
      mid: [150, 150, 150],
      deep: [58, 58, 58],
      smoke: [22, 22, 22],
      sky: [5, 5, 5],
      rim: [235, 235, 235],
      shadow: [14, 14, 14],
    },
  };

  /* ---------- časová osa ---------- */
  /* Vrací hodnotu 0..1 pro úsek [from, to] sekund s danou funkcí náběhu. */
  function span(t, from, to, ease) {
    const raw = U.clamp((t - from) / Math.max(to - from, 1e-6), 0, 1);
    return ease ? ease(raw) : raw;
  }

  /* Celá režie klipu. Vrací sílu jednotlivých vrstev v čase t (v sekundách). */
  function direct(t, dur) {
    const outro = span(t, dur - 1.2, dur, U.easeInOut);      // závěrečné ztmavení kvůli smyčce
    const glow = span(t, 0.0, 1.6, U.easeOutCubic);          // žár zespodu
    const portrait = span(t, 0.9, 2.6, U.easeOutCubic);      // nástup portrétu
    const wings = span(t, 1.6, 4.2, U.easeOutCubic);         // rozevření křídel
    const halo = span(t, 2.4, 4.0, U.easeOutCubic);          // svatozář / prstenec
    const title = span(t, 3.6, 5.4, U.easeOutCubic);         // vypálení titulku
    const sub = span(t, 4.6, 6.0, U.easeOutCubic);           // podtitul
    return {
      t, dur, glow, portrait, wings, halo, title, sub,
      fade: 1 - outro,
      // pomalé "dýchání" scény, ať obraz nikdy nestojí
      breath: Math.sin(t * 0.9) * 0.5 + 0.5,
      flicker: 0.72 + 0.28 * U.noise1(t * 7.3),
    };
  }

  AG.U = U;
  AG.PALETTES = PALETTES;
  AG.span = span;
  AG.direct = direct;
})(window.AG);
