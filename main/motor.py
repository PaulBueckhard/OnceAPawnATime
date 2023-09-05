from time import sleep
from enum import Enum
from miscellaneous.units import Units
try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    pass

units = Units()

class MotorId(Enum):
    motorX = 'motorX'
    motorY = 'motorY'

class Motor:
    def __init__(self, motorId, STEP, DIR, EN):
        self.motorId = motorId
        self.STEP = STEP
        self.DIR = DIR
        self.EN = EN

        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.STEP, GPIO.OUT)
        GPIO.setup(self.DIR, GPIO.OUT)
        GPIO.setup(self.EN, GPIO.OUT)

        GPIO.output(self.EN, GPIO.HIGH)
    
    def step(self, moveSteps, clockDirection, delay=units.MIN_US_DELAY):
        GPIO.output(self.EN, GPIO.LOW)
        GPIO.output(self.DIR, GPIO.HIGH if (clockDirection == 'cw') else GPIO.LOW)

        for i in range(int(moveSteps)):
            GPIO.output(self.STEP, GPIO.HIGH)
            sleep(units.uS * delay)
            GPIO.output(self.STEP, GPIO.LOW)
            sleep(units.uS * delay)

        GPIO.output(self.EN, GPIO.HIGH)