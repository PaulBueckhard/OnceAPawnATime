from miscellaneous.pins import Pins
try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    pass

pins = Pins()

class Magnet:
    def __init__(self):
        self.pin = pins.RELAIS

        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)
