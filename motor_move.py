from time import sleep
import RPi.GPIO as GPIO
from motor import Motor
from motor import Units

""" GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


STEP = 5 # Step GPIO pin
DIR = 3 # Direction GPIO pin
EN = 23 # Enable pin


GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(EN, GPIO.OUT) """

""" # 2400 steps makes about 46.5 cm linear distance (5.1613 steps/mm)
MIN_US_DELAY = 950 # Minimum required delay between steps
usDelay = 950 # number of microseconds
uS = 0.000001 # one microsecond
spmm = 5.1613 # steps/mm
fieldLength = 58 # width and length of a field on the board in mm
# clockwise movement on motor_x is X positive
# counterclockwise movement on motor_x is X negative """
steps = 2000 # Nr of steps
reps = 3 # Nr of times to repeat script 
units = Units()
# print("[press ctrl+c to end the script]")

def move_motor_back_and_forth(steps, reps, units):
    try: # Main program loop
        motorX = Motor('motor_x')
        for i in range(reps):
            motorX.step(steps, 'cw', units.usDelay)
            sleep(1)
            motorX.step(steps, 'ccw', units.usDelay)
            sleep(1)
        #motorX.step(2400, 'ccw', units.usDelay)

    # Scavenging work after the end of the program
    except KeyboardInterrupt:
        GPIO.output(motorX.pins.EN, GPIO.HIGH)

def move_motor_on_board(dif_x, dif_y, units):
    try: 
        motorX = Motor('motor_x')

        if dif_x > 0:
            for i in range(dif_x):
                motorX.step(units.fieldSteps, 'cw', units.usDelay)
        elif dif_x < 0:
            for i in range(dif_x):
                motorX.step(units.fieldSteps, 'ccw', units.usDelay)

    except KeyboardInterrupt:
        GPIO.output(motorX.pins.EN, GPIO.HIGH)