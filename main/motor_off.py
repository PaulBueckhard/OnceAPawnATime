from motor import Motor
from miscellaneous.pins import Pins

try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    pass

pins = Pins()

motorX = Motor('motorX', pins.STEP_X, pins.DIR_X, pins.EN_X)
motorY = Motor('motorY', pins.STEP_Y, pins.DIR_Y, pins.EN_Y)

GPIO.output(motorX.EN, GPIO.HIGH)
GPIO.output(motorY.EN, GPIO.HIGH)