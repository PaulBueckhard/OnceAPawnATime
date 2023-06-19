from miscellaneous.pins import Pins
try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    pass

pins = Pins()

GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers

GPIO.setup(pins.RELAIS, GPIO.OUT) # GPIO Assign mode
GPIO.output(pins.RELAIS, GPIO.LOW) # out
#GPIO.output(pins.RELAIS, GPIO.HIGH) # on
