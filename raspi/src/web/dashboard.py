#!/usr/bin/env python3
import time, json, threading, queue
from flask import Flask, Response, render_template_string
import pigpio

CHANNEL_PINS = {
    "ch1_roll":     4,
    "ch2_pitch":    17,
    "ch3_throttle": 27,
    "ch4_yaw":      5,
    "ch5_mode":     6,
    "ch6_aux":      20,
    "ch7_aux":      21,
}

PULSE_MIN_US = 1000
PULSE_MAX_US = 2000
STALE_AFTER_S = 0.25

app = Flask(__name__)
pi = pigpio.pi()
if not pi.connected:
    raise RuntimeError("pigpio daemon not running. Try: sudo systemctl start pigpiod")

state = { name: {"pin": pin, "pulse_us": 0.0, "norm": 0.0, "age_s": 999.0, "ok": False}
          for name, pin in CHANNEL_PINS.items() }

updates = queue.Queue()

def clamp(x, lo, hi): 
    return lo if x < lo else hi if x > hi else x

def us_to_norm(us):
    us = clamp(us, PULSE_MIN_US, PULSE_MAX_US)
    return (2.0 * (us - PULSE_MIN_US) / (PULSE_MAX_US - PULSE_MIN_US)) - 1.0

class PulseReader:
    def __init__(self, pin, name):
        self.pin = pin
        self.name = name
        self.high_tick = None
        self.last = time.monotonic()
        self.cb = pi.callback(pin, pigpio.EITHER_EDGE, self._cb)

    def _cb(self, gpio, level, tick):
        if level == 1:
            self.high_tick = tick
        elif level == 0 and self.high_tick is not None:
            dt = pigpio.tickDiff(self.high_tick, tick)
            self.high_tick = None
            if 800 <= dt <= 2500:
                s = state[self.name]
                s["pulse_us"] = float(dt)
                s["norm"] = us_to_norm(dt)
                s["age_s"] = 0.0
                s["ok"] = True
                self.last = time.monotonic()
                updates.put(1)

    def poll_stale(self):
        age = time.monotonic() - self.last
        if age > STALE_AFTER_S:
            s = state[self.name]
            s["age_s"] = age
            s["ok"] = False

readers = []
for name, pin in CHANNEL_PINS.items():
    pi.set_mode(pin, pigpio.INPUT)
    pi.set_pull_up_down(pin, pigpio.PUD_DOWN)
    readers.append(PulseReader(pin, name))

def staleness_task():
    while True:
        for r in readers:
            r.poll_stale()
        time.sleep(0.05)

threading.Thread(target=staleness_task, daemon=True).start()

INDEX_HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>RC Receiver Dashboard</title>
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <style>
    body { font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; margin: 24px; background: #0b1220; color: #eef2ff;}
    h1 { margin: 0 0 8px; font-weight: 600; }
    .grid { display:grid; grid-template-columns: repeat(auto-fit,minmax(260px,1fr)); gap:14px; margin-top: 18px;}
    .card { background:#111827; border:1px solid #1f2937; border-radius:14px; padding:14px; box-shadow:0 4px 20px rgba(0,0,0,0.25);}
    .name { font-size:14px; opacity:.85; letter-spacing:.2px; }
    .row { display:flex; align-items:center; gap:10px; margin:8px 0; }
    .barOuter { flex:1; height:16px; background:#0f172a; border-radius:8px; overflow:hidden; border:1px solid #1f2937;}
    .barInner { height:100%; width:50%; background:linear-gradient(90deg,#3b82f6,#22d3ee); transition:width 80ms linear; }
    .val { font-variant-numeric: tabular-nums; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size:13px;}
    .chip { display:inline-block; padding:2px 8px; border-radius:999px; background:#0b1328; border:1px solid #223049; font-size:12px; margin-left:8px;}
    .bad { color:#fca5a5; border-color:#7f1d1d; background:#1c0e10; }
    footer { margin-top:16px; opacity:.7; font-size:12px; }
  </style>
</head>
<body>
  <h1>RC Receiver Dashboard <span id="status" class="chip">connecting…</span></h1>
  <div class="grid" id="grid"></div>
  <footer>Tip: bars show normalized position (−1…+1). Numbers show µs & normalized value. A red chip means a channel hasn’t updated recently.</footer>

<script>
const CHANNELS = {{ channels | safe }};
const grid = document.getElementById('grid');
const statusChip = document.getElementById('status');

function cardTemplate(name) {
  const id = name.replaceAll(/[^a-z0-9_]/g,'_');
  return `
    <div class="card" id="card_${id}">
      <div class="name">${name}</div>
      <div class="row">
        <div class="barOuter"><div class="barInner" id="bar_${id}"></div></div>
        <div class="val" id="val_${id}">—</div>
      </div>
      <div class="chip" id="chip_${id}">fresh</div>
    </div>`;
}

grid.innerHTML = CHANNELS.map(cardTemplate).join('');

function setBar(name, us, norm, ok, age) {
  const id = name.replaceAll(/[^a-z0-9_]/g,'_');
  const w = Math.round((norm + 1) * 50);
  document.getElementById('bar_'+id).style.width = w + '%';
  document.getElementById('val_'+id).textContent = `${Math.round(us)} µs  |  ${norm.toFixed(2)}`;
  const chip = document.getElementById('chip_'+id);
  if (ok) { chip.textContent = 'fresh'; chip.classList.remove('bad'); }
  else { chip.textContent = `stale ${age.toFixed(2)}s`; chip.classList.add('bad'); }
}

function connect() {
  const es = new EventSource('/stream');
  es.onopen = () => { statusChip.textContent = 'live'; };
  es.onerror = () => { statusChip.textContent = 'reconnecting…'; };
  es.onmessage = (ev) => {
    try {
      const data = JSON.parse(ev.data);
      Object.keys(data).forEach(k => {
        const d = data[k];
        setBar(k, d.pulse_us || 0, d.norm || 0, !!d.ok, d.age_s || 0);
      });
    } catch {}
  };
}
connect();
</script>
</body>
</html>
"""

@app.get("/")
def index():
    return render_template_string(INDEX_HTML, channels=list(CHANNEL_PINS.keys()))

@app.get("/stream")
def stream():
    def gen():
        last_push = 0
        while True:
            try:
                now = time.monotonic()
                if now - last_push >= 0.1:
                    last_push = now
                    yield "data: " + json.dumps(state) + "\n\n"
                else:
                    updates.get(timeout=0.1)
            except Exception:
                pass
    return Response(gen(), mimetype="text/event-stream")


if __name__ == "__main__":
    print("Serving on http://0.0.0.0:5000  (Ctrl+C to stop)")
    app.run(host="0.0.0.0", port=5000, threaded=True)
