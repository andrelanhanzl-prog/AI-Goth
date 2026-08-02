/* AI-Goth :: Fiery Angel — jednotlivé vrstvy scény */
window.AG = window.AG || {};

(function (AG) {
  'use strict';
  const U = AG.U;

  /* =========================================================
     POZADÍ — temná obloha, valící se kouř, žhnoucí obzor
     ========================================================= */
  const SMOKE = [];
  for (let i = 0; i < 18; i++) {
    SMOKE.push({
      x: U.hash(i * 3.1),
      y: U.hash(i * 7.7),
      r: 0.28 + U.hash(i * 5.3) * 0.42,
      sp: 0.012 + U.hash(i * 2.1) * 0.035,
      sw: 0.3 + U.hash(i * 9.9) * 1.4,
      dark: U.hash(i * 4.4) > 0.55,
    });
  }

  function drawBackground(ctx, L, P, s) {
    const { W, H, S } = L;
    const d = s.dir, cfg = s.cfg;

    // základní gradient: nahoře skoro černo, dole doutnající obzor
    const g = ctx.createLinearGradient(0, 0, 0, H);
    g.addColorStop(0, U.rgba(P.sky, 1));
    g.addColorStop(0.5, U.rgba(P.smoke, 1));
    g.addColorStop(1, U.rgba(P.deep, 0.85));
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, W, H);

    // žhavý kotouč za postavou (drží se u postavy, nezaplavuje celý obraz)
    const power = (0.22 + 0.30 * cfg.intensity) * d.glow * d.flicker;
    const rg = ctx.createRadialGradient(L.cx, L.cy + S * 0.06, S * 0.02, L.cx, L.cy + S * 0.02, S * 0.62);
    rg.addColorStop(0, U.rgba(P.hot, 0.42 * power));
    rg.addColorStop(0.4, U.rgba(P.mid, 0.20 * power));
    rg.addColorStop(1, U.rgba(P.deep, 0));
    ctx.fillStyle = rg;
    ctx.fillRect(0, 0, W, H);

    // valící se kouř — měkké stoupající chuchvalce
    ctx.save();
    for (let i = 0; i < SMOKE.length; i++) {
      const b = SMOKE[i];
      const p = (b.y + d.t * b.sp) % 1;
      const y = H * (1.15 - p * 1.3);
      const x = W * b.x + Math.sin(d.t * b.sw * 0.35 + i) * S * 0.09;
      const r = S * b.r * (0.7 + p * 0.7);
      const a = Math.sin(p * Math.PI) * 0.32 * cfg.smoke * d.glow;
      if (a <= 0.005) continue;

      ctx.globalCompositeOperation = b.dark ? 'source-over' : 'lighter';
      const bg = ctx.createRadialGradient(x, y, 0, x, y, r);
      if (b.dark) {
        bg.addColorStop(0, U.rgba(P.sky, a * 0.9));
        bg.addColorStop(1, U.rgba(P.sky, 0));
      } else {
        bg.addColorStop(0, U.rgba(P.deep, a * 0.6));
        bg.addColorStop(0.5, U.rgba(P.deep, a * 0.25));
        bg.addColorStop(1, U.rgba(P.deep, 0));
      }
      ctx.fillStyle = bg;
      ctx.beginPath();
      ctx.arc(x, y, r, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.restore();

    // doutnající zem
    const floor = ctx.createLinearGradient(0, H * 0.74, 0, H);
    floor.addColorStop(0, U.rgba(P.deep, 0));
    floor.addColorStop(1, U.rgba(P.mid, 0.22 * d.glow * cfg.intensity));
    ctx.fillStyle = floor;
    ctx.fillRect(0, H * 0.74, W, H * 0.26);
  }

  /* =========================================================
     KŘÍDLA — procedurální ohnivá pera podél zakřivené páteře
     ========================================================= */

  // bod a tečna na kvadratické Bézierově křivce
  function bez(p0, p1, p2, t) {
    const mt = 1 - t;
    return {
      x: mt * mt * p0.x + 2 * mt * t * p1.x + t * t * p2.x,
      y: mt * mt * p0.y + 2 * mt * t * p1.y + t * t * p2.y,
      dx: 2 * mt * (p1.x - p0.x) + 2 * t * (p2.x - p1.x),
      dy: 2 * mt * (p1.y - p0.y) + 2 * t * (p2.y - p1.y),
    };
  }

  /* Jedno pero: prohnutý zúžený tvar mezi kořenem (x,y) a hrotem.
     Nejjasnější je u kořene, hrot se rozpouští v uhlících — proto
     gradient končí průhledností.                                     */
  function featherTo(ctx, x, y, tx, ty, wid, curve, P, alpha, heat) {
    const vx = tx - x, vy = ty - y;
    const len = Math.hypot(vx, vy) || 1;
    const ang = Math.atan2(vy, vx);
    return feather(ctx, x, y, ang, len, wid, curve, P, alpha, heat);
  }

  function feather(ctx, x, y, ang, len, wid, curve, P, alpha, heat) {
    const cos = Math.cos(ang), sin = Math.sin(ang);
    const nx = -sin, ny = cos;                       // normála k ose pera
    const ex = x + cos * len + nx * curve * len;     // prohnutý hrot
    const ey = y + sin * len + ny * curve * len;

    const g = ctx.createLinearGradient(x, y, ex, ey);
    g.addColorStop(0.00, U.rgba(P.hot, 0.40 * alpha * heat));
    g.addColorStop(0.18, U.rgba(P.mid, 0.30 * alpha));
    g.addColorStop(0.48, U.rgba(P.deep, 0.16 * alpha));
    g.addColorStop(0.78, U.rgba(P.deep, 0.05 * alpha));
    g.addColorStop(1.00, U.rgba(P.deep, 0));

    // obrys: dvě křivky od kořene ke hrotu, největší šířka v první třetině
    const m1x = x + cos * len * 0.32 + nx * curve * len * 0.25;
    const m1y = y + sin * len * 0.32 + ny * curve * len * 0.25;
    ctx.beginPath();
    ctx.moveTo(x + nx * wid * 0.35, y + ny * wid * 0.35);
    ctx.quadraticCurveTo(m1x + nx * wid, m1y + ny * wid, ex, ey);
    ctx.quadraticCurveTo(m1x - nx * wid * 0.85, m1y - ny * wid * 0.85,
      x - nx * wid * 0.35, y - ny * wid * 0.35);
    ctx.closePath();
    ctx.fillStyle = g;
    ctx.fill();

    // žhavý stvol pera — jen náznak, jinak by křídlo vypadalo jako hřeben
    const cg = ctx.createLinearGradient(x, y, ex, ey);
    cg.addColorStop(0, U.rgba(P.core, 0.22 * alpha * heat));
    cg.addColorStop(0.25, U.rgba(P.hot, 0.12 * alpha));
    cg.addColorStop(1, U.rgba(P.mid, 0));
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.quadraticCurveTo(m1x, m1y, ex, ey);
    ctx.lineWidth = Math.max(1, wid * 0.18);
    ctx.strokeStyle = cg;
    ctx.stroke();

    return { ex, ey };
  }

  /* Křídlo je vymezené dvěma křivkami: náběžnou hranou (od ramene ke
     zápěstí) a odtokovou hranou (od boku ke špičce letek). Pero číslo u
     vede z jednoho bodu na druhý — díky tomu pera vyplní tvar křídla
     místo aby se rozevřela do vějíře.                                  */
  const WING_SHAPE = {
    shoulder: { x: 0.00, y: 0.00 },   // kořen křídla za ramenem
    leadCtrl: { x: 0.08, y: -0.95 },  // náběžná hrana stoupá skoro svisle
    wrist: { x: 0.72, y: -1.15 },     // „zápěstí“ vysoko a stranou
    base: { x: 0.02, y: 0.55 },       // spodek vnitřních letek
    trailCtrl: { x: 0.62, y: 0.55 },  // odtoková hrana zůstává nízko
    tip: { x: 1.05, y: -0.35 },       // špičky letek ven a mírně vzhůru
  };

  /* Řady per, odzadu dopředu: dlouhé letky vespod, krátká krycí pera
     u ramene navrchu. `reach` je podíl vzdálenosti k odtokové hraně. */
  const WING_ROWS = [
    { n: 26, from: 0.04, to: 1.00, reach: 1.00, wid: 0.062, curve: 0.16, alpha: 0.95 },
    { n: 22, from: 0.02, to: 0.86, reach: 0.66, wid: 0.056, curve: 0.13, alpha: 0.78 },
    { n: 18, from: 0.00, to: 0.62, reach: 0.38, wid: 0.048, curve: 0.10, alpha: 0.62 },
  ];

  // jedno křídlo; dirSign = +1 vpravo, -1 vlevo
  function wing(ctx, L, P, s, dirSign) {
    const { S } = L;
    const d = s.dir, cfg = s.cfg;
    const open = d.wings;
    if (open <= 0.001) return;

    /* Asymetrie: obě křídla mají jinou velikost, náklon i posazení —
       symetrický obraz působí jako logo, ne jako zjevení.             */
    const asym = cfg.asym;
    const right = dirSign > 0;
    const span = L.wingLen * cfg.wingSize * (right ? 1 + 0.26 * asym : 1 - 0.20 * asym);
    const ax = L.cx + dirSign * S * (right ? 0.10 : 0.12);
    const ay = L.cy - S * 0.02 + S * (right ? -0.06 : 0.05) * asym;
    const tilt = (right ? -0.16 : 0.22) * asym;

    // rozevření: z přitisknuté polohy se křídlo odklápí nahoru a do stran
    const spread = U.mix(0.34, 1.0, open);
    const phase = right ? 0 : 1.9;
    const flap = Math.sin(d.t * 0.75 + phase) * 0.05 + (U.noise1(d.t * 1.4 + dirSign * 3) - 0.5) * 0.05;

    // řídicí body tvaru přepočtené do pixelů; `spread` křídlo rozevírá
    const K = WING_SHAPE;
    const wx = 1 + (right ? 0.06 : -0.09) * asym;
    const wy = 1 + (right ? 0.10 : -0.12) * asym;
    const pt = (p, sy) => ({
      x: p.x * span * U.mix(0.55, 1, spread) * wx,
      y: p.y * span * spread * wy * (1 + (sy ? flap : 0)),
    });
    const SH = pt(K.shoulder), LC = pt(K.leadCtrl, 1), WR = pt(K.wrist, 1);
    const BA = pt(K.base), TC = pt(K.trailCtrl), TP = pt(K.tip, 1);

    ctx.save();
    ctx.translate(ax, ay);
    ctx.scale(dirSign, 1);
    ctx.rotate(tilt);
    ctx.globalCompositeOperation = 'lighter';

    // měkká záře, aby křídla svítila do okolí
    const halo = ctx.createRadialGradient(span * 0.42, -span * 0.5, S * 0.01, span * 0.42, -span * 0.5, span * 1.0);
    halo.addColorStop(0, U.rgba(P.mid, 0.14 * open * cfg.intensity));
    halo.addColorStop(0.5, U.rgba(P.deep, 0.08 * open));
    halo.addColorStop(1, U.rgba(P.deep, 0));
    ctx.fillStyle = halo;
    ctx.fillRect(-span * 0.6, -span * 1.8, span * 2.4, span * 2.6);

    /* Vědomě tu není žádná plná výplň tvaru — jakmile se křídlo vyplní,
       ztratí okraj a začne vypadat jako mušle. Hmotu drží jen měkká záře
       a překryv per, hranici tvoří jejich nestejně dlouhé hroty.        */

    for (let r = 0; r < WING_ROWS.length; r++) {
      const row = WING_ROWS[r];
      for (let i = 0; i < row.n; i++) {
        const k = i / (row.n - 1);
        const u = U.mix(row.from, row.to, k);

        // pera vyrůstají postupně od ramene ke špičce
        const grow = U.clamp((open - 0.08 - u * 0.5) / 0.42, 0, 1);
        if (grow <= 0) continue;

        const seed = i * 1.7 + r * 31.3 + dirSign * 5.1;
        const flick = 0.70 + 0.55 * U.noise1(d.t * 4.2 + seed);
        const jitter = (U.hash(seed) - 0.5);
        if (U.hash(seed * 2.3) < 0.06) continue;      // pár mezer, ať to není pravidelné

        const a = bez(SH, LC, WR, u);                 // kořen na náběžné hraně
        const b = bez(BA, TC, TP, U.clamp(u + jitter * 0.05, 0, 1));  // hrot na odtokové

        /* Délka se u každého pera liší a ještě se v čase mění — jinak by
           hroty splynuly v hladký oblouk a z křídla by byl vějíř.      */
        const wave = U.noise1(d.t * 1.8 + i * 0.9 + r * 7.7);
        const reach = row.reach * grow * (0.72 + U.hash(seed * 1.9) * 0.52) *
          (0.86 + 0.28 * wave) * (0.88 + 0.2 * cfg.intensity);
        const tx = a.x + (b.x - a.x) * reach;
        const ty = a.y + (b.y - a.y) * reach;
        const wid = span * row.wid * (0.8 + 0.4 * flick) * grow;
        // vnější pera se stáčejí víc dozadu — křídlo tím dostane oblouk
        const curve = row.curve * (0.55 + k * 0.9) * (1 + jitter * 0.5);

        const tip = featherTo(ctx, a.x, a.y, tx, ty, wid, curve,
          P, row.alpha * grow * d.fade * (0.62 + 0.3 * cfg.intensity), flick);

        // žhavý kořen pera — rozbije souvislou světlou linku náběžné hrany
        if (r === 0 || r === 2) {
          const br = wid * 0.9;
          const bgz = ctx.createRadialGradient(a.x, a.y, 0, a.x, a.y, br);
          bgz.addColorStop(0, U.rgba(P.core, 0.30 * grow * flick * d.fade));
          bgz.addColorStop(0.5, U.rgba(P.hot, 0.14 * grow * d.fade));
          bgz.addColorStop(1, U.rgba(P.mid, 0));
          ctx.fillStyle = bgz;
          ctx.beginPath();
          ctx.arc(a.x, a.y, br, 0, Math.PI * 2);
          ctx.fill();
        }

        // z hrotů letek odletují jiskry
        if (r === 0 && U.noise1(d.t * 2.6 + seed * 3.1) > 0.74) {
          const sp = S * 0.005 * flick;
          const sg = ctx.createRadialGradient(tip.ex, tip.ey, 0, tip.ex, tip.ey, sp * 3);
          sg.addColorStop(0, U.rgba(P.core, 0.5 * grow));
          sg.addColorStop(1, U.rgba(P.hot, 0));
          ctx.fillStyle = sg;
          ctx.beginPath();
          ctx.arc(tip.ex, tip.ey, sp * 3, 0, Math.PI * 2);
          ctx.fill();
        }
      }
    }

    // pár dlouhých šlehů, které vystřelí za špičky letek
    for (let i = 0; i < 7; i++) {
      const u = 0.45 + i * 0.08;
      const seed = i * 13.7 + dirSign * 2.3;
      const n = U.noise1(d.t * 1.1 + seed);
      if (n < 0.35) continue;
      const a = bez(SH, LC, WR, u);
      const b = bez(BA, TC, TP, U.clamp(u + 0.05, 0, 1));
      const reach = (1.15 + n * 0.45) * open;
      featherTo(ctx, a.x, a.y, a.x + (b.x - a.x) * reach, a.y + (b.y - a.y) * reach,
        span * 0.016, 0.34, P, 0.5 * open * d.fade, 1);
    }

    ctx.restore();
  }

  function drawWings(ctx, L, P, s) {
    wing(ctx, L, P, s, -1);
    wing(ctx, L, P, s, 1);
  }

  /* =========================================================
     PORTRÉT — duotón, maska, obrysové světlo, vlnění žáru
     ========================================================= */
  const off = document.createElement('canvas');
  const offCtx = off.getContext('2d');
  const off2 = document.createElement('canvas');
  const off2Ctx = off2.getContext('2d');

  function drawPortrait(ctx, L, P, s) {
    const img = s.image;
    const d = s.dir, cfg = s.cfg;
    const { S } = L;
    const box = {
      w: L.portraitW * cfg.photoScale,
      h: L.portraitW * cfg.photoScale * 1.28,
    };
    box.x = L.cx - box.w / 2 + cfg.photoX * S;
    box.y = L.cy - box.h * 0.52 + cfg.photoY * S;

    if (off.width !== Math.ceil(box.w) || off.height !== Math.ceil(box.h)) {
      off.width = off2.width = Math.max(2, Math.ceil(box.w));
      off.height = off2.height = Math.max(2, Math.ceil(box.h));
    }
    const w = off.width, h = off.height;
    offCtx.clearRect(0, 0, w, h);

    if (img) {
      // výřez "cover" + volitelné otočení fotky (mobilní snímky bývají na bok)
      offCtx.save();
      const rot = (cfg.photoRotate * Math.PI) / 180;
      offCtx.translate(w / 2, h / 2 + h * cfg.photoFraming);
      offCtx.rotate(rot);
      const rw = Math.abs(Math.cos(rot)) * w + Math.abs(Math.sin(rot)) * h;
      const rh = Math.abs(Math.sin(rot)) * w + Math.abs(Math.cos(rot)) * h;
      const scale = Math.max(rw / img.width, rh / img.height);
      const dw = img.width * scale, dh = img.height * scale;
      offCtx.drawImage(img, -dw / 2, -dh / 2, dw, dh);
      offCtx.restore();
    } else {
      // zástupná silueta, dokud není nahraná fotka
      const g = offCtx.createLinearGradient(0, 0, 0, h);
      g.addColorStop(0, '#2a2226');
      g.addColorStop(1, '#0d0a0c');
      offCtx.fillStyle = g;
      offCtx.fillRect(0, 0, w, h);
      offCtx.fillStyle = '#000';
      offCtx.beginPath();
      offCtx.ellipse(w / 2, h * 0.34, w * 0.20, h * 0.17, 0, 0, Math.PI * 2);
      offCtx.fill();
      offCtx.beginPath();
      offCtx.moveTo(w * 0.5, h * 0.46);
      offCtx.bezierCurveTo(w * 0.02, h * 0.62, w * 0.06, h, w * 0.12, h);
      offCtx.lineTo(w * 0.88, h);
      offCtx.bezierCurveTo(w * 0.94, h, w * 0.98, h * 0.62, w * 0.5, h * 0.46);
      offCtx.fill();
    }

    // --- barevná gradace: duotón (jas fotky × ohnivá paleta) ---
    if (cfg.duotone > 0) {
      off2Ctx.clearRect(0, 0, w, h);
      const dg = off2Ctx.createLinearGradient(0, 0, 0, h);
      dg.addColorStop(0, U.rgba(P.hot, 1));
      dg.addColorStop(0.45, U.rgba(P.mid, 1));
      dg.addColorStop(1, U.rgba(P.shadow, 1));
      off2Ctx.fillStyle = dg;
      off2Ctx.fillRect(0, 0, w, h);
      off2Ctx.globalCompositeOperation = 'luminosity';
      off2Ctx.drawImage(off, 0, 0);
      off2Ctx.globalCompositeOperation = 'source-over';

      offCtx.globalAlpha = cfg.duotone;
      offCtx.drawImage(off2, 0, 0);
      offCtx.globalAlpha = 1;
    }

    // ztmavení okolí, aby ze tmy vystoupil jen obličej
    const fx = w * (0.5 + cfg.focusX);
    const fy = h * (0.42 + cfg.focusY);
    const vg = offCtx.createRadialGradient(fx, fy, w * 0.10 * cfg.focus, fx, fy, w * 0.85 * cfg.focus);
    vg.addColorStop(0, 'rgba(0,0,0,0)');
    vg.addColorStop(0.45, 'rgba(0,0,0,' + (0.30 + 0.45 * cfg.contrast) + ')');
    vg.addColorStop(1, 'rgba(0,0,0,' + (0.72 + 0.28 * cfg.contrast) + ')');
    offCtx.fillStyle = vg;
    offCtx.fillRect(0, 0, w, h);

    // obrysové světlo od ohně
    offCtx.globalCompositeOperation = 'lighter';
    const rimL = offCtx.createLinearGradient(0, 0, w * 0.40, 0);
    rimL.addColorStop(0, U.rgba(P.rim, 0.34 * cfg.intensity * d.flicker));
    rimL.addColorStop(1, 'rgba(0,0,0,0)');
    offCtx.fillStyle = rimL;
    offCtx.fillRect(0, 0, w, h);
    const rimR = offCtx.createLinearGradient(w, 0, w * 0.60, 0);
    rimR.addColorStop(0, U.rgba(P.hot, 0.26 * cfg.intensity * (1.4 - d.flicker)));
    rimR.addColorStop(1, 'rgba(0,0,0,0)');
    offCtx.fillStyle = rimR;
    offCtx.fillRect(0, 0, w, h);
    const under = offCtx.createLinearGradient(0, h, 0, h * 0.6);
    under.addColorStop(0, U.rgba(P.mid, 0.30 * cfg.intensity));
    under.addColorStop(1, 'rgba(0,0,0,0)');
    offCtx.fillStyle = under;
    offCtx.fillRect(0, 0, w, h);
    offCtx.globalCompositeOperation = 'source-over';

    // maska tvaru
    offCtx.globalCompositeOperation = 'destination-in';
    if (cfg.mask === 'oval') {
      const m = offCtx.createRadialGradient(fx, fy, w * 0.10 * cfg.focus, fx, fy, w * 0.56 * cfg.focus);
      m.addColorStop(0, 'rgba(0,0,0,1)');
      m.addColorStop(0.55, 'rgba(0,0,0,0.95)');
      m.addColorStop(1, 'rgba(0,0,0,0)');
      offCtx.fillStyle = m;
      offCtx.fillRect(0, 0, w, h);
    } else if (cfg.mask === 'burn') {
      const m = offCtx.createLinearGradient(0, 0, 0, h);
      m.addColorStop(0, 'rgba(0,0,0,0.10)');
      m.addColorStop(0.20, 'rgba(0,0,0,1)');
      m.addColorStop(0.62, 'rgba(0,0,0,1)');
      m.addColorStop(1, 'rgba(0,0,0,0)');
      offCtx.fillStyle = m;
      offCtx.fillRect(0, 0, w, h);
      // nepravidelný okraj hoření
      for (let x = 0; x < w; x += 3) {
        const n = U.fbm(x / 60, d.t * 0.7, 3);
        const cut = h * (0.68 + n * 0.24);
        offCtx.clearRect(x, cut, 4, h - cut);
      }
      // boční změkčení
      const sm = offCtx.createLinearGradient(0, 0, w, 0);
      sm.addColorStop(0, 'rgba(0,0,0,0)');
      sm.addColorStop(0.14, 'rgba(0,0,0,1)');
      sm.addColorStop(0.86, 'rgba(0,0,0,1)');
      sm.addColorStop(1, 'rgba(0,0,0,0)');
      offCtx.globalCompositeOperation = 'destination-in';
      offCtx.fillStyle = sm;
      offCtx.fillRect(0, 0, w, h);
    }
    offCtx.globalCompositeOperation = 'source-over';

    /* Temná hmota ramen pod portrétem — bez ní hlava visí v prázdnu.
       Splývá s pozadím, takže jen naznačí postavu ustupující do tmy.  */
    if (cfg.bodyShadow > 0.01) {
      ctx.save();
      ctx.globalAlpha = d.portrait * d.fade * cfg.bodyShadow;
      const byy = box.y + box.h * 0.78;
      const bw = box.w * 0.95, bh = box.h * 0.85;
      const bgr = ctx.createRadialGradient(L.cx, byy, bw * 0.08, L.cx, byy, bw * 0.75);
      bgr.addColorStop(0, 'rgba(0,0,0,0.92)');
      bgr.addColorStop(0.55, 'rgba(0,0,0,0.55)');
      bgr.addColorStop(1, 'rgba(0,0,0,0)');
      ctx.fillStyle = bgr;
      ctx.beginPath();
      ctx.ellipse(L.cx + S * 0.02 * cfg.asym, byy + bh * 0.25, bw * 0.75, bh * 0.7, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }

    // --- vykreslení do scény, případně přes vlnění horkého vzduchu ---
    ctx.save();
    ctx.globalAlpha = d.portrait * d.fade;
    const bob = Math.sin(d.t * 0.8) * S * 0.004;
    const scale = U.mix(1.06, 1, d.portrait);
    ctx.translate(box.x + box.w / 2, box.y + box.h / 2 + bob);
    ctx.scale(scale, scale);
    ctx.translate(-box.w / 2, -box.h / 2);

    if (cfg.heat > 0.01) {
      const sl = 8;
      for (let y = 0; y < h; y += sl) {
        const amp = cfg.heat * S * 0.010 * U.smoothstep(0, 1, y / h);
        const dxo = Math.sin(y * 0.035 + d.t * 3.4) * amp +
          (U.noise1(y * 0.06 + d.t * 2.2) - 0.5) * amp * 1.6;
        ctx.drawImage(off, 0, y, w, sl, dxo, y, w, sl);
      }
    } else {
      ctx.drawImage(off, 0, 0);
    }
    ctx.restore();

    L.portraitBox = box;
    L.focusPoint = { x: box.x + fx, y: box.y + fy };
  }

  /* =========================================================
     SVATOZÁŘ — prstenec nad hlavou
     ========================================================= */
  function drawHalo(ctx, L, P, s) {
    const d = s.dir, cfg = s.cfg;
    if (!cfg.halo || d.halo <= 0.001) return;
    const { S } = L;
    const box = L.portraitBox;
    const cx = L.focusPoint.x + S * 0.05 * cfg.asym;
    const cy = box.y + box.h * cfg.haloY;
    const r = S * 0.14 * cfg.wingSize * d.halo;
    const tilt = 0.28;
    const roll = -0.16 * cfg.asym;          // svatozář visí nakřivo

    ctx.save();
    ctx.globalCompositeOperation = 'lighter';
    ctx.globalAlpha = d.halo * d.fade;
    ctx.translate(cx, cy);
    ctx.rotate(roll);

    for (let i = 0; i < 3; i++) {
      ctx.beginPath();
      ctx.ellipse(0, 0, r * (1 + i * 0.03), r * tilt * (1 + i * 0.05), 0, 0, Math.PI * 2);
      ctx.lineWidth = S * (0.009 - i * 0.0028);
      ctx.strokeStyle = U.rgba(i === 0 ? P.core : P.hot, (0.45 - i * 0.13) * d.flicker);
      ctx.stroke();
    }
    for (let i = 0; i < 22; i++) {
      const a = (i / 22) * Math.PI * 2 + d.t * 0.9;
      const px = Math.cos(a) * r, py = Math.sin(a) * r * tilt;
      const sz = S * 0.0035 * (0.5 + U.noise1(i * 3.7 + d.t * 6));
      ctx.fillStyle = U.rgba(P.core, 0.6);
      ctx.beginPath();
      ctx.arc(px, py, sz, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.restore();
  }

  /* =========================================================
     UHLÍKY A PLAMENY
     ========================================================= */
  function makeEmbers(n) {
    const arr = [];
    for (let i = 0; i < n; i++) {
      arr.push({
        seed: i,
        x: U.hash(i * 1.7),
        life: U.hash(i * 4.3),
        speed: 0.06 + U.hash(i * 9.1) * 0.16,
        size: 0.25 + U.hash(i * 5.5) * 1.0,
        sway: 0.4 + U.hash(i * 2.9) * 1.6,
        big: U.hash(i * 11.3) > 0.93,
      });
    }
    return arr;
  }

  function drawEmbers(ctx, L, P, s, embers, front) {
    const { W, H, S } = L;
    const d = s.dir, cfg = s.cfg;
    ctx.save();
    ctx.globalCompositeOperation = 'lighter';
    ctx.globalAlpha = d.fade;

    for (let i = 0; i < embers.length; i++) {
      const e = embers[i];
      if ((e.seed % 2 === 0) !== front) continue;
      const p = (e.life + d.t * e.speed * cfg.emberSpeed) % 1;   // 0 dole → 1 nahoře
      const y = H * (1.04 - p * 1.12);
      // uhlíky stoupají šikmo — vane vítr z jedné strany
      const x = W * e.x + Math.sin(d.t * e.sway + e.seed) * S * 0.05 * (0.3 + p) +
        p * S * 0.10 * cfg.asym;
      const a = Math.sin(p * Math.PI) * (front ? 0.75 : 0.45) * cfg.emberAmount * d.glow *
        U.clamp(1 + cfg.asym * (e.x - 0.4), 0.25, 1.8);
      if (a <= 0.01) continue;
      const r = S * 0.0032 * e.size * (front ? 1.2 : 0.8) * (e.big ? 2.2 : 1);

      const g = ctx.createRadialGradient(x, y, 0, x, y, r * 4);
      g.addColorStop(0, U.rgba(P.core, a));
      g.addColorStop(0.3, U.rgba(P.hot, a * 0.6));
      g.addColorStop(1, U.rgba(P.mid, 0));
      ctx.fillStyle = g;
      ctx.beginPath();
      ctx.arc(x, y, r * 4, 0, Math.PI * 2);
      ctx.fill();

      if (e.big) {   // ohon u velkých jisker
        ctx.strokeStyle = U.rgba(P.hot, a * 0.3);
        ctx.lineWidth = r * 0.9;
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(x - Math.sin(d.t * e.sway + e.seed) * S * 0.008, y + S * 0.03);
        ctx.stroke();
      }
    }
    ctx.restore();
  }

  /* plameny olizující spodní okraj — nepravidelné, ne pilovité */
  const TONGUES = [];
  for (let i = 0; i < 22; i++) {
    TONGUES.push({
      x: U.hash(i * 6.1),
      w: 0.5 + U.hash(i * 2.7) * 1.3,
      h: 0.45 + U.hash(i * 8.3) * 1.1,
      sp: 0.8 + U.hash(i * 3.9) * 2.2,
      ph: U.hash(i * 5.7) * 10,
    });
  }

  function drawFlames(ctx, L, P, s) {
    const { W, H, S } = L;
    const d = s.dir, cfg = s.cfg;
    if (cfg.intensity <= 0.02) return;
    ctx.save();
    ctx.globalCompositeOperation = 'lighter';
    ctx.globalAlpha = d.glow * d.fade;

    for (let i = 0; i < TONGUES.length; i++) {
      const f = TONGUES[i];
      const n = U.noise1(d.t * f.sp + f.ph);
      const x = f.x * W + Math.sin(d.t * 0.6 + f.ph) * S * 0.02;
      // oheň hoří silněji na jedné straně — nikdy ne rovnoměrně přes celý spodek
      const bias = U.clamp(1 + cfg.asym * 1.3 * (f.x - 0.42), 0.15, 2.2);
      const hgt = S * 0.20 * f.h * (0.35 + n * 0.85) * cfg.intensity * bias;
      const wdt = S * 0.035 * f.w * (0.7 + n * 0.5);
      const lean = Math.sin(d.t * 1.3 + f.ph) * wdt * 0.9;

      const g = ctx.createLinearGradient(x, H, x, H - hgt);
      g.addColorStop(0, U.rgba(P.hot, 0.30));
      g.addColorStop(0.35, U.rgba(P.mid, 0.18));
      g.addColorStop(1, U.rgba(P.deep, 0));
      ctx.fillStyle = g;
      ctx.beginPath();
      ctx.moveTo(x - wdt, H + 2);
      ctx.bezierCurveTo(x - wdt * 0.9, H - hgt * 0.45, x + lean - wdt * 0.3, H - hgt * 0.75, x + lean, H - hgt);
      ctx.bezierCurveTo(x + lean + wdt * 0.3, H - hgt * 0.75, x + wdt * 0.9, H - hgt * 0.45, x + wdt, H + 2);
      ctx.closePath();
      ctx.fill();
    }
    ctx.restore();
  }

  /* =========================================================
     TEXT — vypálený titulek s ohnivým gradientem
     ========================================================= */
  function fitText(ctx, text, font, maxW, startPx) {
    let px = startPx;
    for (let i = 0; i < 60; i++) {
      ctx.font = font.replace('__PX__', px);
      if (ctx.measureText(text).width <= maxW || px < 12) break;
      px -= Math.max(1, px * 0.04);
    }
    return px;
  }

  function drawText(ctx, L, P, s) {
    const { W, H, S } = L;
    const d = s.dir, cfg = s.cfg;
    const title = (cfg.title || '').toUpperCase();
    const sub = cfg.subtitle || '';
    if (!title && !sub) return;

    ctx.save();
    // text schválně nesedí v ose obrazu — kotví se vlevo, vpravo nebo na střed
    const pad = W * 0.075;
    const ax = cfg.textAlign === 'left' ? pad
      : cfg.textAlign === 'right' ? W - pad
        : W / 2 + W * 0.03 * cfg.asym;
    ctx.textAlign = cfg.textAlign === 'center' ? 'center' : cfg.textAlign;
    ctx.globalAlpha = d.fade;
    const y = H - S * cfg.titleY;

    /* --- titulek --- */
    if (title && d.title > 0.001) {
      const fontTpl = '900 __PX__px ' + cfg.font;
      const px = fitText(ctx, title, fontTpl, W - pad * 2, S * 0.15);
      ctx.font = fontTpl.replace('__PX__', px);

      const grad = ctx.createLinearGradient(0, y - px * 0.85, 0, y + px * 0.15);
      grad.addColorStop(0, U.rgba(P.core, 1));
      grad.addColorStop(0.40, U.rgba(P.hot, 1));
      grad.addColorStop(0.78, U.rgba(P.mid, 1));
      grad.addColorStop(1, U.rgba(P.deep, 1));

      // maska „vypalování“ — text se objevuje odspodu nahoru
      ctx.save();
      const revealH = px * 2.2;
      const rTop = y + px * 0.32 - revealH * U.easeOutCubic(d.title);
      ctx.beginPath();
      ctx.rect(0, rTop, W, H);
      ctx.clip();

      ctx.shadowColor = U.rgba(P.mid, 0.9);
      ctx.shadowBlur = px * 0.5 * d.flicker;
      ctx.fillStyle = grad;
      ctx.fillText(title, ax, y);
      ctx.shadowBlur = px * 0.18;
      ctx.fillText(title, ax, y);
      ctx.shadowBlur = 0;
      ctx.lineWidth = Math.max(1, px * 0.010);
      ctx.strokeStyle = U.rgba(P.core, 0.28);
      ctx.strokeText(title, ax, y);
      ctx.restore();

      /* Žhavá hrana právě „hořícího“ řádku. Drží se jen na šířce nápisu
         a jen po dobu, kdy opravdu prochází písmeny.                   */
      if (d.title < 1 && rTop > y - px * 0.78 && rTop < y + px * 0.30) {
        const tw = ctx.measureText(title).width;
        const x0 = cfg.textAlign === 'left' ? ax
          : cfg.textAlign === 'right' ? ax - tw : ax - tw / 2;
        ctx.save();
        ctx.globalCompositeOperation = 'lighter';
        const eg = ctx.createLinearGradient(x0, 0, x0 + tw, 0);
        eg.addColorStop(0, U.rgba(P.hot, 0));
        eg.addColorStop(0.2, U.rgba(P.core, 0.34));
        eg.addColorStop(0.8, U.rgba(P.core, 0.34));
        eg.addColorStop(1, U.rgba(P.hot, 0));
        ctx.fillStyle = eg;
        ctx.shadowColor = U.rgba(P.hot, 0.9);
        ctx.shadowBlur = px * 0.35;
        ctx.fillRect(x0, rTop - px * 0.035, tw, px * 0.07);
        ctx.restore();
      }

      L.titleSize = px;
    }

    /* --- podtitul --- */
    if (sub && d.sub > 0.001) {
      const fontTpl = '500 __PX__px ' + cfg.font;
      const px = fitText(ctx, sub, fontTpl, W - pad * 2.4, S * 0.038);
      ctx.font = fontTpl.replace('__PX__', px);
      ctx.globalAlpha = d.sub * d.fade;
      if ('letterSpacing' in ctx) ctx.letterSpacing = (px * 0.26) + 'px';
      ctx.shadowColor = U.rgba(P.mid, 0.8);
      ctx.shadowBlur = px * 0.8;
      ctx.fillStyle = U.rgba(P.core, 0.88);
      ctx.fillText(sub.toUpperCase(), ax, y + (L.titleSize || px * 2) * 0.62 + px * 1.1);
      if ('letterSpacing' in ctx) ctx.letterSpacing = '0px';
    }

    ctx.restore();
  }

  /* =========================================================
     FINÁLNÍ ÚPRAVY — vinětace, zrno, ztmavení do smyčky
     ========================================================= */
  function drawGrade(ctx, L, P, s) {
    const { W, H, S } = L;
    const d = s.dir, cfg = s.cfg;

    // vinětace není souměrná — světlo přichází z jedné strany
    const vx = L.cx + S * 0.10 * cfg.asym, vy = L.cy - S * 0.05 * cfg.asym;
    const v = ctx.createRadialGradient(vx, vy, S * 0.28, vx, vy, S * 0.95);
    v.addColorStop(0, 'rgba(0,0,0,0)');
    v.addColorStop(1, 'rgba(0,0,0,' + (0.30 + 0.45 * cfg.vignette) + ')');
    ctx.fillStyle = v;
    ctx.fillRect(0, 0, W, H);

    // filmové zrno
    if (cfg.grain > 0.01) {
      const step = 3;
      ctx.save();
      ctx.globalAlpha = cfg.grain * 0.30;
      const fr = Math.floor(d.t * 24);
      for (let y = 0; y < H; y += step) {
        for (let x = 0; x < W; x += step) {
          const n = U.hash2(x * 0.37 + fr, y * 0.71);
          if (n > 0.90) {
            ctx.fillStyle = n > 0.96 ? 'rgba(255,235,210,0.45)' : 'rgba(0,0,0,0.45)';
            ctx.fillRect(x, y, step, step);
          }
        }
      }
      ctx.restore();
    }

    // nájezd ze tmy a závěrečné ztmavení (kvůli čisté smyčce)
    const a = Math.max(1 - d.fade, 1 - U.smoothstep(0, 0.5, d.t));
    if (a > 0.001) {
      ctx.fillStyle = 'rgba(0,0,0,' + a + ')';
      ctx.fillRect(0, 0, W, H);
    }
  }

  AG.layers = {
    drawBackground, drawWings, drawPortrait, drawHalo,
    drawEmbers, drawFlames, drawText, drawGrade, makeEmbers,
  };
})(window.AG);
