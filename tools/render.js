// Exact-size SVG -> PNG renderer driving Chromium over CDP (no npm deps).
const { spawn } = require('child_process');
const fs = require('fs');
const http = require('http');
const net = require('net');
const crypto = require('crypto');

const [SVG, OUT, W, H, SCALE] = [
  process.argv[2], process.argv[3],
  parseInt(process.argv[4], 10), parseInt(process.argv[5], 10),
  parseFloat(process.argv[6] || '2'),
];

const svg = fs.readFileSync(SVG, 'utf8');
const html = `<!doctype html><meta charset="utf-8"><style>
html,body{margin:0;padding:0;background:#0d0520;overflow:hidden}
svg{display:block;width:${W}px;height:${H}px}
</style>${svg}`;

const pageServer = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
  res.end(html);
});

function get(url) {
  return new Promise((resolve, reject) => {
    http.get(url, r => { let b = ''; r.on('data', d => b += d); r.on('end', () => resolve(JSON.parse(b))); })
      .on('error', reject);
  });
}

// Minimal RFC6455 client: text frames out (masked), frames in reassembled.
function connectWS(wsUrl) {
  return new Promise((resolve, reject) => {
    const u = new URL(wsUrl);
    const key = crypto.randomBytes(16).toString('base64');
    const sock = net.connect(Number(u.port), u.hostname, () => {
      sock.write(
        `GET ${u.pathname}${u.search} HTTP/1.1\r\nHost: ${u.host}\r\nUpgrade: websocket\r\n` +
        `Connection: Upgrade\r\nSec-WebSocket-Key: ${key}\r\nSec-WebSocket-Version: 13\r\n\r\n`
      );
    });
    let buf = Buffer.alloc(0), upgraded = false, frag = [];
    const handlers = new Map();
    let nextId = 1;

    const api = {
      send(method, params = {}) {
        const id = nextId++;
        const payload = Buffer.from(JSON.stringify({ id, method, params }));
        const mask = crypto.randomBytes(4);
        const len = payload.length;
        let head;
        if (len < 126) head = Buffer.from([0x81, 0x80 | len]);
        else if (len < 65536) { head = Buffer.alloc(4); head[0] = 0x81; head[1] = 0xFE; head.writeUInt16BE(len, 2); }
        else { head = Buffer.alloc(10); head[0] = 0x81; head[1] = 0xFF; head.writeBigUInt64BE(BigInt(len), 2); }
        const masked = Buffer.from(payload);
        for (let i = 0; i < masked.length; i++) masked[i] ^= mask[i % 4];
        sock.write(Buffer.concat([head, mask, masked]));
        return new Promise((res, rej) => handlers.set(id, { res, rej }));
      },
      close() { sock.destroy(); },
    };

    sock.on('data', chunk => {
      buf = Buffer.concat([buf, chunk]);
      if (!upgraded) {
        const i = buf.indexOf('\r\n\r\n');
        if (i === -1) return;
        buf = buf.subarray(i + 4);
        upgraded = true;
        resolve(api);
      }
      while (buf.length >= 2) {
        const fin = (buf[0] & 0x80) !== 0, opcode = buf[0] & 0x0f;
        let len = buf[1] & 0x7f, off = 2;
        if (len === 126) { if (buf.length < 4) return; len = buf.readUInt16BE(2); off = 4; }
        else if (len === 127) { if (buf.length < 10) return; len = Number(buf.readBigUInt64BE(2)); off = 10; }
        if (buf.length < off + len) return;
        const payload = buf.subarray(off, off + len);
        buf = buf.subarray(off + len);
        if (opcode === 0x8) { sock.destroy(); return; }
        frag.push(Buffer.from(payload));
        if (!fin) continue;
        const text = Buffer.concat(frag).toString('utf8'); frag = [];
        let msg; try { msg = JSON.parse(text); } catch { continue; }
        if (msg.id && handlers.has(msg.id)) {
          const h = handlers.get(msg.id); handlers.delete(msg.id);
          msg.error ? h.rej(new Error(JSON.stringify(msg.error))) : h.res(msg.result);
        }
      }
    });
    sock.on('error', reject);
  });
}

const sleep = ms => new Promise(r => setTimeout(r, ms));

pageServer.listen(0, '127.0.0.1', async () => {
  const pagePort = pageServer.address().port;
  const devPort = 9000 + Math.floor(Math.random() * 900);
  const chrome = spawn('/opt/pw-browsers/chromium-1194/chrome-linux/chrome', [
    '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars',
    `--remote-debugging-port=${devPort}`, '--remote-allow-origins=*',
    'about:blank',
  ], { stdio: ['ignore', 'ignore', 'ignore'] });

  let target = null;
  for (let i = 0; i < 60 && !target; i++) {
    await sleep(250);
    try {
      const list = await get(`http://127.0.0.1:${devPort}/json/list`);
      target = list.find(t => t.type === 'page');
    } catch { /* not up yet */ }
  }
  if (!target) { console.error('chrome devtools did not start'); process.exit(1); }

  const ws = await connectWS(target.webSocketDebuggerUrl);
  await ws.send('Page.enable');
  await ws.send('Emulation.setDeviceMetricsOverride', {
    width: W, height: H, deviceScaleFactor: 1, mobile: false,
  });
  await ws.send('Page.navigate', { url: `http://127.0.0.1:${pagePort}/` });
  await sleep(1500);
  const shot = await ws.send('Page.captureScreenshot', {
    format: 'png',
    clip: { x: 0, y: 0, width: W, height: H, scale: SCALE },
    captureBeyondViewport: true,
    optimizeForSpeed: false,
  });
  fs.writeFileSync(OUT, Buffer.from(shot.data, 'base64'));
  ws.close(); chrome.kill(); pageServer.close();
  const st = fs.statSync(OUT);
  console.log(`OK ${OUT} ${(st.size / 1024).toFixed(0)} KB @ ${W * SCALE}x${H * SCALE}`);
  process.exit(0);
});
