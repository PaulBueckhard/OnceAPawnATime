from gpiozero import Button
import time
import motor_move
from miscellaneous.units import Units
from miscellaneous.pins import Pins
from motor import Motor

try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    pass

units = Units()
pins = Pins()

x_endstop = Button(pins.ENDSTOP_X, True)
y_endstop = Button(pins.ENDSTOP_Y, True)

motorX = Motor('motorX', pins.STEP_X, pins.DIR_X, pins.EN_X)
motorY = Motor('motorY', pins.STEP_Y, pins.DIR_Y, pins.EN_Y)

def test_y_endstop():

    print("Please press the endstop")

    while True:

        if y_endstop.is_pressed:
            print("Endstop pressed")
            break


def home_robot():
    home_x()
    home_y()


def home_x():

    while True:

        try:
            motorX.step(10, 'cw', units.usDelay)

        except KeyboardInterrupt:
            GPIO.output(motorX.EN, GPIO.HIGH)

        if x_endstop.is_pressed:
            break


def home_y():

    if y_endstop.is_pressed:
        return

    while True:

        motorY.step(10, 'cw', units.usDelay)

        if y_endstop.is_pressed:
            break



def move_left():

    motorY.step(900, 'ccw', units.usDelay)


def move_white_pawn():

    magnet_on()

    motorY.step(640, 'ccw', units.usDelay)

    magnet_off()

def magnet_on():
    GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers

    GPIO.setup(pins.RELAIS, GPIO.OUT) # GPIO Assign mode
    GPIO.output(pins.RELAIS, GPIO.HIGH) # on


def magnet_off():
    GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers

    GPIO.setup(pins.RELAIS, GPIO.OUT) # GPIO Assign mode
    GPIO.output(pins.RELAIS, GPIO.LOW) # off


def move_black_pawn():

    motorY.step(850, 'ccw', units.usDelay)

    magnet_on()

    motorY.step(640, 'cw', units.usDelay)

    magnet_off()

def reset():

    magnet_on()

    motorY.step(640, 'ccw', units.usDelay)

    magnet_off()

    motorY.step(850, 'cw', units.usDelay)


    magnet_on()

    motorY.step(640, 'cw', units.usDelay)

    magnet_off()



#move_left()

#time.sleep(1)

#magnet_off()

# home_y()

def move_demo():

    magnet_on()

    motorY.step((units.fieldSteps * 1), "ccw", units.usDelay) # 1 nach unten

    motorX.step((units.fieldSteps * 1), "cw", units.usDelay) # 1 nach rechts

    magnet_off()

    motorX.step((units.fieldSteps * 1), "ccw", units.usDelay) # 1 nach links

    motorY.step((units.fieldSteps * 4), "ccw", units.usDelay) # 4 nach unten

    magnet_on()

    motorY.step((units.fieldSteps * 1), "cw", units.usDelay) # 1 nach oben

    magnet_off()

    time.sleep(4)

    magnet_on()

    motorY.step((units.fieldSteps * 1), "ccw", units.usDelay) # 1 nach unten

    magnet_off()

    motorY.step((units.fieldSteps * 4), "cw", units.usDelay) # 4 nach oben

    motorX.step((units.fieldSteps * 1), "cw", units.usDelay) # 1 nach rechts

    magnet_on()

    motorX.step((units.fieldSteps * 1), "ccw", units.usDelay) # 1 nach links

    motorY.step((units.fieldSteps * 1), "cw", units.usDelay) # 1 nach oben

    magnet_off()


while True:
    move_demo()
    time.sleep(4)