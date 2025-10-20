
<div align="center">
  <a href="{{ '/' | relative_url }}">Overview</a> ·
  <a href="{{ '/build-log.html' | relative_url }}">Build&nbsp;Log</a> ·
  <a href="{{ '/electronics.html' | relative_url }}">Electronics</a> ·
  <a href="{{ '/code.html' | relative_url }}">Code</a> ·
  <a href="{{ '/mechanical.html' | relative_url }}">Mechanical</a> ·
  <a href="{{ '/gallery.html' | relative_url }}">Gallery</a>
</div>

---

# Build Log

This page is chronological. Add new entries to the **top** so the latest appears first.

---

## 2025-10-20 — Receiver → Pi Dashboard Online
**What happened:** Verified 7-channel PWM input via pigpio. Built a lightweight Flask dashboard with SSE.  
**Media:** ![Dashboard](assets/images/dashboard-placeholder.jpg)  
**Notes:** Reversed CH3, disabled throttle→elevator mix on the Futaba.  
**Lessons Learned:** Keep a "clean baseline" profile on the TX. Document µs endpoints per channel.  
**Next Step:** Map ballast valves and gimbal toggle in software.

---

## 2025-10-19 — Voltage Divider Board
**What happened:** Hand-built resistor ladder to level-shift RX signals to 3V3.  
**Media:** ![PCB](assets/images/pcb-placeholder.jpg)  
**Notes:** Messy but functional; next rev improves labeling and strain relief.  
**Lessons Learned:** Star-ground saves headaches. Keep wire lengths short to reduce jitter.  
**Next Step:** Mount on a standoff rail inside the hull.
