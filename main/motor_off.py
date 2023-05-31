from motor import Motor
from miscellaneous.units import Units

try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    pass


motorX = Motor('motor_x')
motorY = Motor('motor_y')

GPIO.output(motorX.pins.EN, GPIO.HIGH)
GPIO.output(motorY.pins.EN, GPIO.HIGH)