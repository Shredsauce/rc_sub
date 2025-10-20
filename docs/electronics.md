
<div align="center">
  <a href="{{ '/' | relative_url }}">Overview</a> ·
  <a href="{{ '/build-log.html' | relative_url }}">Build&nbsp;Log</a> ·
  <a href="{{ '/electronics.html' | relative_url }}">Electronics</a> ·
  <a href="{{ '/code.html' | relative_url }}">Code</a> ·
  <a href="{{ '/mechanical.html' | relative_url }}">Mechanical</a> ·
  <a href="{{ '/gallery.html' | relative_url }}">Gallery</a>
</div>

---

# Electronics

## Receiver → Pi Pin Map
```
CH1 roll      → GPIO 4
CH2 pitch     → GPIO 17
CH3 throttle  → GPIO 27
CH4 yaw       → GPIO 5
CH5 mode      → GPIO 6
CH6 aux       → GPIO 20
CH7 aux       → GPIO 21
```
> Source: see `/raspi/rc_dashboard.py`

![RX Wiring](assets/images/rx-wiring-placeholder.jpg)

### Lessons Learned
- Tie grounds together (receiver, Pi, ESC/servos).
- Keep RC signal leads short; add 0.01 µF to GND if jittery.

### Next Step
- Route ESC signal + dedicated BEC rail; isolate servo power from logic 3V3.
