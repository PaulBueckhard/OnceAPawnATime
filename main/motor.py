from time import sleep
from enum import Enum
from miscellaneous.pins import Pins
from miscellaneous.units import Units

try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    pass

units = Units()
    
class MotorId(Enum):
    motorX = 'motorX'
    motorY = 'motorY'

class MotorX:

    def __init__(self, motorId):
        self.motorId: MotorId = motorId
        self.pins = Pins(motorId)
        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.pins.STEP_X, GPIO.OUT)
        GPIO.setup(self.pins.DIR_X, GPIO.OUT)
        GPIO.setup(self.pins.EN_X, GPIO.OUT)
    
    # makes motor move number of steps given, clockwise if clockDirection is "cw", counterclockwise if anything else, at speed of delay
    def step(self, moveSteps, clockDirection, delay=units.MIN_US_DELAY):
        GPIO.output(self.pins.EN_X, GPIO.LOW)

        GPIO.output(self.pins.DIR_X, GPIO.HIGH if (clockDirection == 'cw') else GPIO.LOW)


        for i in range(moveSteps):
            GPIO.output(self.pins.STEP_X, GPIO.HIGH)
            sleep(units.uS * delay)
            GPIO.output(self.pins.STEP_X, GPIO.LOW)
            sleep(units.uS * delay)
            verboseDir = 'clockwise' if (clockDirection == 'cw') else 'counterclockwise'


	#print(f"moved {moveSteps} steps {verboseDir}")

        GPIO.output(self.pins.EN_X, GPIO.HIGH)



    def travel(self, distance, direction):
        stepNr = round(distance * spmm)
        step(stepNr, clockDirection)
    
class MotorY:

    def __init__(self, motorId):
        self.motorId: MotorId = motorId
        self.pins = Pins(motorId)
        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.pins.STEP_Y, GPIO.OUT)
        GPIO.setup(self.pins.DIR_Y, GPIO.OUT)
        GPIO.setup(self.pins.EN_Y, GPIO.OUT)
    
    # makes motor move number of steps given, clockwise if clockDirection is "cw", counterclockwise if anything else, at speed of delay
    def step(self, moveSteps, clockDirection, delay=units.MIN_US_DELAY):
        GPIO.output(self.pins.EN_Y, GPIO.LOW)

        GPIO.output(self.pins.DIR_Y, GPIO.HIGH if (clockDirection == 'cw') else GPIO.LOW)


        for i in range(moveSteps):
            GPIO.output(self.pins.STEP_Y, GPIO.HIGH)
            sleep(units.uS * delay)
            GPIO.output(self.pins.STEP_Y, GPIO.LOW)
            sleep(units.uS * delay)
            verboseDir = 'clockwise' if (clockDirection == 'cw') else 'counterclockwise'


	#print(f"moved {moveSteps} steps {verboseDir}")

        GPIO.output(self.pins.EN_Y, GPIO.HIGH)