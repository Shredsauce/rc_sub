from ..config import SERVO_RUDDER_X1, SERVO_RUDDER_X2
from ..actuators.servo import Servo

class Rudders:
    def __init__(self, pi, rx):
        self.rx = rx
        self.x1 = Servo(pi, SERVO_RUDDER_X1)  # CH1 roll
        self.x2 = Servo(pi, SERVO_RUDDER_X2)  # CH2 pitch
        self.rev_roll = False
        self.rev_pitch = False

    def step(self):
        roll_us, _  = self.rx.get("roll")
        pitch_us, _ = self.rx.get("pitch")
        if self.rev_roll:  roll_us  = 3000 - roll_us
        if self.rev_pitch: pitch_us = 3000 - pitch_us
        self.x1.write_us(roll_us)
        self.x2.write_us(pitch_us)

    def stop(self):
        self.x1.neutral(); self.x2.neutral()
