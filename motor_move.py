from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


STEP = 5 # Step GPIO pin
DIR = 3 # Direction GPIO pin
EN = 23 # Enable pin


GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(EN, GPIO.OUT)

# 2400 steps makes about 46.5 cm linear distance
MIN_US_DELAY = 950 # Minimum required delay between steps
steps = 2000 # number of steps
usDelay = 950 # number of microseconds
uS = 0.000001 # one microsecond


# makes motor move number of steps given, clockwise if direction is "cw", counterclockwise if anything else, at speed of delay
def motor_step(steps, direction, delay=MIN_US_DELAY):
    GPIO.output(EN, GPIO.LOW)

    GPIO.output(DIR, GPIO.HIGH if (direction == "cw") else GPIO.LOW)
    for i in range(steps):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(uS * delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(uS * delay)
    
    GPIO.output(EN, GPIO.HIGH)

#
print("[press ctrl+c to end the script]")

try: # Main program loop
    for i in range(3):
        motor_step(steps, "cw", usDelay)
        sleep(1)
        motor_step(steps, "ccw", usDelay)
        sleep(1)
    #motor_step(2400, "ccw", usDelay)

# Scavenging work after the end of the program
except KeyboardInterrupt:
    GPIO.output(EN, GPIO.HIGH)