import time, pigpio
from .config import CHANNEL_PINS, STALE_AFTER_S

class RCReceiver:
    def __init__(self, pi: pigpio.pi):
        self.pi = pi
        self.state = {k: {"us":1500, "ok":False, "last":0.0, "_rise":None} for k in CHANNEL_PINS}
        for name, pin in CHANNEL_PINS.items():
            pi.set_mode(pin, pigpio.INPUT); pi.set_pull_up_down(pin, pigpio.PUD_DOWN)
            pi.callback(pin, pigpio.EITHER_EDGE, self._cb_factory(name))

    def _cb_factory(self, name):
        def cb(gpio, level, tick):
            s = self.state[name]
            if level == 1: s["_rise"] = tick
            elif level == 0 and s.get("_rise") is not None:
                dt = pigpio.tickDiff(s["_rise"], tick)
                if 800 <= dt <= 2500:
                    s["us"] = float(dt); s["ok"] = True; s["last"] = time.monotonic()
        return cb

    def get(self, name, default=1500):
        s = self.state[name]
        if time.monotonic() - s["last"] > STALE_AFTER_S: s["ok"] = False; s["us"] = default
        return s["us"], s["ok"]
