
<div align="center">
  <a href="{{ '/' | relative_url }}">Overview</a> ·
  <a href="{{ '/build-log.html' | relative_url }}">Build&nbsp;Log</a> ·
  <a href="{{ '/electronics.html' | relative_url }}">Electronics</a> ·
  <a href="{{ '/code.html' | relative_url }}">Code</a> ·
  <a href="{{ '/mechanical.html' | relative_url }}">Mechanical</a> ·
  <a href="{{ '/gallery.html' | relative_url }}">Gallery</a>
</div>

---

# Code

- **Dashboard:** `/raspi/rc_dashboard.py` — Flask + pigpio, streams channel pulse widths and normalized values over SSE.
- Planned: mixer layer to map TX channels to subsystem outputs (ESC, servos, valves).

```bash
# Setup on Pi (first time)
ssh pi@<pi-host>
cd ~/rcsub
make setup    # installs pigpio, creates venv, installs Flask
make run      # runs the dashboard locally
make service  # installs & enables systemd service
```
Then open:
```
http://<pi-ip>:5000
```

### Lessons Learned
- SSE is dead simple and reliable for telemetry.
- Normalize to [-1..+1] early; it simplifies mixers.

### Next Step
- Add output drivers (pigpio `set_servo_pulsewidth`) with safety arming.
