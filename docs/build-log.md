
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


Mapped out controls:

Right stick horizontal: CH1  
Right stick vertical: CH2  
Left stick vertical: CH3  
Back left spring toggle: CH4  
Gear toggle: CH5  
Left knob: CH6  
Right knob: CH7  

I would have loved to have the ballast tank controls on the right knob (channel 7). Right next to the knob is the 2->6, 6->2 MIX switch. The switch has three states: Up, middle, and down. I would have liked to have it like this:  
* MIX switch up: Only fore ballast affected  
* MIX switch middle: Both ballasts affected  
* MIX switch down: Only aft ballast affected  

This is impossible set with the transmitter unfortunately. I *could* reroute the switch somehow but it doesn't seem worth it.
I've settled on using the spring toggle in back (SNAP ROLL ON). I've disabled all other channels except for channel 4. By default, turning the ballast knob will affect both ballast tanks. But if the switch is pulled back, only one tank is affected. This tank is determined by the channel 5 switch (GEAR) 
