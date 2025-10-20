
<div align="center">
  <a href="{{ '/' | relative_url }}">Overview</a> ·
  <a href="{{ '/build-log.html' | relative_url }}">Build&nbsp;Log</a> ·
  <a href="{{ '/electronics.html' | relative_url }}">Electronics</a> ·
  <a href="{{ '/code.html' | relative_url }}">Code</a> ·
  <a href="{{ '/mechanical.html' | relative_url }}">Mechanical</a> ·
  <a href="{{ '/gallery.html' | relative_url }}">Gallery</a>
</div>

---

# RC Submarine Project

> An experimental radio-controlled submarine exploring underwater control systems, magnetic couplers, and a Pi-based telemetry stack.

![Hero](assets/images/hero-placeholder.jpg)

## Goals
- Reliable sealed hull with serviceable internals
- Clean radio stack: Futaba → voltage divider → Raspberry Pi (telemetry + control)
- X-rudder actuation and camera gimbal
- Ballast system (fill/empty, independent fore/aft)
- Document the journey (successes *and* failures)

## Current Status (snapshot)
- ✅ Receiver → Pi dashboard shows clean, unmixed PWM
- 🚧 Ballast control mapping and valve logic
- 🧪 Magnetic coupler alignment & sealing tests

## Key Links
- [Build Log](build-log.md)
- [Electronics](electronics.md)
- [Code](code.md)
- [Mechanical](mechanical.md)
- [Gallery](gallery.md)

## How to Read This Site
This is a **living engineering notebook**. The [Build Log](build-log.md) is chronological; the topic pages deep-dive into subsystems. Each page ends with *Lessons Learned* and *Next Step*.
