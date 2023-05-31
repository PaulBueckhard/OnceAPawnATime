from gpiozero import Button
import time
import motor_move
from miscellaneous.units import Units
from motor import MotorX, MotorY

try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    pass


y_endstop = Button(21, True)
x_endstop = Button(19, True)
units = Units()



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
            motorX = MotorX('motor_x')
            motorX.step(10, 'cw', units.usDelay)

        except KeyboardInterrupt:
            GPIO.output(motorX.pins.EN, GPIO.HIGH)

        if x_endstop.is_pressed:
            break


def home_y():

    if y_endstop.is_pressed:
        return

    while True:

        motorY = MotorY('motor_y')
        motorY.step(10, 'cw', units.usDelay)

        if y_endstop.is_pressed:
            break



def move_left():

    motorY = MotorX('motor_y')
    motorY.step(900, 'ccw', units.usDelay)


def move_white_pawn():

    magnet_on()

    motorY = MotorX('motor_y')
    motorY.step(640, 'ccw', units.usDelay)

    magnet_off()

def magnet_on():
    GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers

    RELAIS_1_GPIO = 27
    GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode
    GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # on


def magnet_off():
    GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers

    RELAIS_1_GPIO = 27
    GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode
    GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # off


def move_black_pawn():

    motorY = MotorX('motor_y')
    motorY.step(850, 'ccw', units.usDelay)

    magnet_on()

    motorY.step(640, 'cw', units.usDelay)

    magnet_off()

def reset():

    magnet_on()

    motorY = MotorX('motor_y')
    motorY.step(640, 'ccw', units.usDelay)

    magnet_off()

    motorY.step(850, 'cw', units.usDelay)


    magnet_on()

    motorY = MotorX('motor_y')
    motorY.step(640, 'cw', units.usDelay)

    magnet_off()



#move_left()

#time.sleep(1)

# magnet_off()

# home_y()

# time.sleep(1)

# move_white_pawn()

# move_black_pawn()

# magnet_off()

# time.sleep(1)

# reset()


