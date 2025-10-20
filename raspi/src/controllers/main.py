#!/usr/bin/env python3
import time, signal, pigpio
from ..rc_input import RCReceiver
from .rudders import Rudders

running = True
def _stop(*_): 
    global running; running = False

def main():
    pi = pigpio.pi()
    if not pi.connected:
        raise SystemExit("pigpiod not running (sudo systemctl start pigpiod)")
    rx = RCReceiver(pi)
    rudders = Rudders(pi, rx)

    signal.signal(signal.SIGINT, _stop); signal.signal(signal.SIGTERM, _stop)
    try:
        while running:
            rudders.step()
            time.sleep(0.02)  # 50 Hz
    finally:
        rudders.stop(); pi.stop()

if __name__ == "__main__":
    main()
