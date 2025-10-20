import pigpio
from ..config import SERVO_MIN, SERVO_MAX

def clamp(v, lo, hi): return lo if v<lo else hi if v>hi else v

class Servo:
    def __init__(self, pi: pigpio.pi, gpio: int):
        self.pi = pi; self.gpio = gpio
        self.pi.set_mode(gpio, pigpio.OUTPUT)

    def write_us(self, us: float):
        self.pi.set_servo_pulsewidth(self.gpio, clamp(us, SERVO_MIN, SERVO_MAX))

    def neutral(self, mid=1500): self.write_us(mid)
