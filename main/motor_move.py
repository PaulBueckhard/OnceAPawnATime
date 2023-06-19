from time import sleep
from motor import Motor
from miscellaneous.units import Units
from miscellaneous.pins import Pins
try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    pass

pins = Pins()
units = Units()

motorX = Motor('motorX', pins.STEP_X, pins.DIR_X, pins.EN_X)
motorY = Motor('motorY', pins.STEP_Y, pins.DIR_Y, pins.EN_Y)

class Motor_move:
    def move_motor_on_board(dif_x, dif_y, units):
        try: 
            if dif_x > 0:
                travelFields = units.fieldSteps * dif_x
                motorX.step(travelFields, 'cw', units.usDelay)

            elif dif_x < 0:
                travelFields = units.fieldSteps * dif_x * -1
                motorX.step(travelFields, 'ccw', units.usDelay)

            if dif_y > 0:
                travelFields = units.fieldSteps * dif_y
                motorY.step(travelFields, 'cw', units.usDelay)

            elif dif_y < 0:
                travelFields = units.fieldSteps * dif_y * -1
                motorY.step(travelFields, 'ccw', units.usDelay)

        except KeyboardInterrupt:
            GPIO.output(motorX.EN, GPIO.HIGH)
            GPIO.output(motorY.EN, GPIO.HIGH)

    def manual_movement():
        move_x = int(input("X-Coordinate: "))
        move_y = int(input("Y-Coordinate: "))

        Motor_move.move_motor_on_board(move_x, move_y, units)

Motor_move.manual_movement()

# 192.168.170.9