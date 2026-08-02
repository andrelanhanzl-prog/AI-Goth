/* AI-Goth :: Fiery Angel — ovládání, přehrávání, export */
(function (AG) {
  'use strict';

  const U = AG.U;
  const canvas = document.getElementById('stage');
  const ctx = canvas.getContext('2d', { alpha: false });

  const cfg = Object.assign({}, AG.scene.DEFAULTS);
  let image = null;
  let playing = true;
  let time = 0;
  let last = performance.now();
  let recorder = null;

  const $ = (id) => document.getElementById(id);
  const scrub = $('scrub');
  const timeLabel = $('timeLabel');

  /* ---------- rozměry plátna ---------- */
  function applyFormat() {
    const dim = AG.scene.FORMATS[cfg.format];
    canvas.width = dim[0];
    canvas.height = dim[1];
    canvas.style.aspectRatio = dim[0] + ' / ' + dim[1];
  }

  /* ---------- smyčka ---------- */
  function frame(now) {
    const dt = Math.min((now - last) / 1000, 0.05);
    last = now;
    if (playing) time = (time + dt * cfg.speedFactor) % cfg.duration;

    AG.scene.render(ctx, cfg, image, time);

    scrub.value = String((time / cfg.duration) * 1000);
    timeLabel.textContent = time.toFixed(1) + ' s / ' + cfg.duration + ' s';
    requestAnimationFrame(frame);
  }
  cfg.speedFactor = 1;

  /* ---------- napojení ovládacích prvků ---------- */
  function bindRange(id, key, transform) {
    const el = $(id);
    if (!el) return;
    el.value = String(transform ? transform.to(cfg[key]) : cfg[key]);
    const out = $(id + 'Val');
    const show = () => { if (out) out.textContent = el.value; };
    show();
    el.addEventListener('input', () => {
      cfg[key] = transform ? transform.from(parseFloat(el.value)) : parseFloat(el.value);
      show();
    });
  }

  function bindText(id, key) {
    const el = $(id);
    el.value = cfg[key];
    el.addEventListener('input', () => { cfg[key] = el.value; });
  }

  function bindSelect(id, key, after) {
    const el = $(id);
    el.value = cfg[key];
    el.addEventListener('change', () => {
      cfg[key] = el.value;
      if (after) after();
    });
  }

  bindText('title', 'title');
  bindText('subtitle', 'subtitle');
  bindSelect('palette', 'palette');
  bindSelect('format', 'format', applyFormat);
  bindSelect('mask', 'mask');
  bindSelect('font', 'font');
  bindSelect('textAlign', 'textAlign');

  bindRange('asym', 'asym');

  bindRange('intensity', 'intensity');
  bindRange('wingSize', 'wingSize');
  bindRange('emberAmount', 'emberAmount');
  bindRange('emberSpeed', 'emberSpeed');
  bindRange('smoke', 'smoke');
  bindRange('heat', 'heat');
  bindRange('duotone', 'duotone');
  bindRange('contrast', 'contrast');
  bindRange('bodyShadow', 'bodyShadow');
  bindRange('vignette', 'vignette');
  bindRange('grain', 'grain');
  bindRange('photoScale', 'photoScale');
  bindRange('photoX', 'photoX');
  bindRange('photoY', 'photoY');
  bindRange('photoRotate', 'photoRotate');
  bindRange('photoFraming', 'photoFraming');
  bindRange('focus', 'focus');
  bindRange('focusX', 'focusX');
  bindRange('focusY', 'focusY');
  bindRange('haloY', 'haloY');
  bindRange('titleY', 'titleY');
  bindRange('duration', 'duration');
  bindRange('speedFactor', 'speedFactor');

  $('halo').checked = cfg.halo;
  $('halo').addEventListener('change', (e) => { cfg.halo = e.target.checked; });

  /* ---------- fotka ---------- */
  function loadFile(file) {
    if (!file || !/^image\//.test(file.type)) return;
    const reader = new FileReader();
    reader.onload = () => {
      const img = new Image();
      img.onload = () => {
        image = img;
        $('dropHint').classList.add('hidden');
        // na výšku otočené fotky z telefonu: nabídneme rychlé narovnání
        $('photoInfo').textContent = img.width + '×' + img.height + ' px';
      };
      img.src = reader.result;
    };
    reader.readAsDataURL(file);
  }

  $('photo').addEventListener('change', (e) => loadFile(e.target.files[0]));

  const drop = $('viewport');
  ['dragenter', 'dragover'].forEach((ev) =>
    drop.addEventListener(ev, (e) => { e.preventDefault(); drop.classList.add('dragging'); })
  );
  ['dragleave', 'drop'].forEach((ev) =>
    drop.addEventListener(ev, (e) => { e.preventDefault(); drop.classList.remove('dragging'); })
  );
  drop.addEventListener('drop', (e) => {
    if (e.dataTransfer.files && e.dataTransfer.files[0]) loadFile(e.dataTransfer.files[0]);
  });

  /* rychlé otočení fotky po 90° (mobilní snímky bývají na bok) */
  $('rotate90').addEventListener('click', () => {
    cfg.photoRotate = (cfg.photoRotate + 90) % 360;
    $('photoRotate').value = String(cfg.photoRotate);
    const out = $('photoRotateVal');
    if (out) out.textContent = String(cfg.photoRotate);
  });

  /* ---------- přehrávání ---------- */
  $('playPause').addEventListener('click', (e) => {
    playing = !playing;
    e.target.textContent = playing ? '⏸ Pauza' : '▶ Přehrát';
  });
  $('restart').addEventListener('click', () => { time = 0; });
  scrub.addEventListener('input', () => {
    playing = false;
    $('playPause').textContent = '▶ Přehrát';
    time = (parseFloat(scrub.value) / 1000) * cfg.duration;
  });

  /* ---------- export snímku ---------- */
  $('snap').addEventListener('click', () => {
    AG.scene.render(ctx, cfg, image, time);
    canvas.toBlob((blob) => download(blob, 'ai-goth-snimek.png'), 'image/png');
  });

  function download(blob, name) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = name;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 4000);
  }

  /* ---------- nahrávání videa ---------- */
  function pickMime() {
    const list = [
      'video/webm;codecs=vp9',
      'video/webm;codecs=vp8',
      'video/webm',
      'video/mp4',
    ];
    for (const m of list) {
      if (window.MediaRecorder && MediaRecorder.isTypeSupported(m)) return m;
    }
    return '';
  }

  const recBtn = $('record');
  recBtn.addEventListener('click', () => {
    if (recorder) { recorder.stop(); return; }
    if (!canvas.captureStream || !window.MediaRecorder) {
      alert('Tento prohlížeč neumí nahrávat plátno. Zkus Chrome nebo Edge, případně použij OBS a nahraj okno.');
      return;
    }
    const mime = pickMime();
    const stream = canvas.captureStream(60);
    const chunks = [];
    recorder = new MediaRecorder(stream, mime ? { mimeType: mime, videoBitsPerSecond: 12000000 } : undefined);
    recorder.ondataavailable = (e) => { if (e.data.size) chunks.push(e.data); };
    recorder.onstop = () => {
      const ext = (recorder.mimeType || '').indexOf('mp4') >= 0 ? 'mp4' : 'webm';
      download(new Blob(chunks, { type: recorder.mimeType }), 'ai-goth-ohnivy-andel.' + ext);
      recorder = null;
      recBtn.textContent = '⏺ Nahrát video';
      recBtn.classList.remove('recording');
      document.body.classList.remove('busy');
    };

    // nahráváme přesně jednu smyčku od začátku
    time = 0;
    playing = true;
    $('playPause').textContent = '⏸ Pauza';
    recorder.start();
    recBtn.textContent = '⏹ Zastavit (nahrává…)';
    recBtn.classList.add('recording');
    document.body.classList.add('busy');
    setTimeout(() => { if (recorder) recorder.stop(); }, (cfg.duration / cfg.speedFactor) * 1000 + 250);
  });

  /* ---------- předvolby ---------- */
  const PRESETS = {
    lucifer: { palette: 'lucifer', intensity: 0.85, wingSize: 1.0, halo: true, mask: 'oval', duotone: 0.8, heat: 0.5, title: 'LUCIFER', subtitle: 'světlonoš' },
    inferno: { palette: 'hellfire', intensity: 1.0, wingSize: 1.15, halo: false, mask: 'burn', duotone: 1.0, heat: 0.85, grain: 0.5 },
    seraph: { palette: 'lucifer', intensity: 0.6, wingSize: 1.25, halo: true, mask: 'oval', duotone: 0.45, heat: 0.25, grain: 0.2, title: 'SERAPH' },
    abyss: { palette: 'abyss', intensity: 0.8, wingSize: 1.05, halo: true, mask: 'oval', duotone: 0.9, heat: 0.4 },
    ash: { palette: 'ash', intensity: 0.7, wingSize: 1.0, halo: false, mask: 'burn', duotone: 1.0, heat: 0.35, grain: 0.6 },
  };

  document.querySelectorAll('[data-preset]').forEach((btn) => {
    btn.addEventListener('click', () => {
      Object.assign(cfg, PRESETS[btn.dataset.preset]);
      syncUI();
      time = 0;
    });
  });

  function syncUI() {
    document.querySelectorAll('input[type=range]').forEach((el) => {
      if (cfg[el.id] !== undefined) {
        el.value = String(cfg[el.id]);
        const out = $(el.id + 'Val');
        if (out) out.textContent = el.value;
      }
    });
    document.querySelectorAll('select').forEach((el) => {
      if (cfg[el.id] !== undefined) el.value = cfg[el.id];
    });
    $('title').value = cfg.title;
    $('subtitle').value = cfg.subtitle;
    $('halo').checked = cfg.halo;
    applyFormat();
  }

  /* ---------- panel skrytí (pro čistý náhled / záznam obrazovky) ---------- */
  $('togglePanel').addEventListener('click', () => {
    document.body.classList.toggle('panel-hidden');
  });

  /* ---------- programové rozhraní ----------
     Umožňuje šablonu řídit z konzole nebo ze skriptu (dávkové generování,
     automatické náhledy): AG.api.set({title:'…'}); AG.api.seek(4.2);        */
  AG.api = {
    cfg,
    set(patch) { Object.assign(cfg, patch); syncUI(); },
    seek(t) { time = U.clamp(t, 0, cfg.duration); playing = false; AG.scene.render(ctx, cfg, image, time); },
    play() { playing = true; },
    pause() { playing = false; },
    setImage(src) {
      return new Promise((res, rej) => {
        const img = new Image();
        img.onload = () => { image = img; $('dropHint').classList.add('hidden'); res(img); };
        img.onerror = rej;
        img.src = src;
      });
    },
    canvas,
  };

  /* ---------- start ---------- */
  applyFormat();
  syncUI();
  requestAnimationFrame(frame);
})(window.AG);
