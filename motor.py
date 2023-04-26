from time import sleep
import RPi.GPIO as GPIO
from enum import Enum
from pins import Pins
from units import Units
units = Units()
    
class MotorId(Enum):
    motorX = 'motorX'
    motorY = 'motorY'

class Motor:    
    """ STEP = 5 # Step GPIO pin
    DIR = 3 # Direction GPIO pin
    EN = 23 # Enable pin """
    
    
    def __init__(self, motorId):
        self.motorId: MotorId = motorId
        self.pins = Pins(motorId)
        self.setup()
        
    
    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.pins.STEP, GPIO.OUT)
        GPIO.setup(self.pins.DIR, GPIO.OUT)
        GPIO.setup(self.pins.EN, GPIO.OUT)
    
    # makes motor move number of steps given, clockwise if clockDirection is "cw", counterclockwise if anything else, at speed of delay
    def step(self, moveSteps, clockDirection, delay=units.MIN_US_DELAY):
        GPIO.output(self.pins.EN, GPIO.LOW)

        GPIO.output(self.pins.DIR, GPIO.HIGH if (clockDirection == 'cw') else GPIO.LOW)
        for i in range(moveSteps):
            GPIO.output(self.pins.STEP, GPIO.HIGH)
            sleep(units.uS * delay)
            GPIO.output(self.pins.STEP, GPIO.LOW)
            sleep(units.uS * delay)
            verboseDir = 'clockwise' if (clockDirection == 'cw') else 'counterclockwise'
        print(f"moved {moveSteps} steps {verboseDir}")
        
        GPIO.output(self.pins.EN, GPIO.HIGH)

    def travel(self, distance, direction):
        stepNr = round(distance * spmm)
        step(stepNr, clockDirection)
    