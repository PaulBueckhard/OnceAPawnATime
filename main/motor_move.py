from time import sleep
from threading import Thread
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
<<<<<<< HEAD
            travelFieldsX = units.fieldSteps * abs(dif_x)
            travelFieldsY = units.fieldSteps * abs(dif_y)
            
=======
            # Knight Movement
>>>>>>> 00d382c410b568bd56ebc0b0997a1c7b13986c60
            if (dif_x == 2) and (dif_y == 1):
                motorY.step((travelFieldsY / 2), 'cw', units.usDelay)
                motorX.step(travelFieldsX, 'cw', units.usDelay)
                motorY.step((travelFieldsY / 2), 'cw', units.usDelay)
            
            elif (dif_x == 1) and (dif_y == 2):
                motorX.step((travelFieldsX / 2), 'cw', units.usDelay)
                motorY.step(travelFieldsY, 'cw', units.usDelay)
                motorX.step((travelFieldsX / 2), 'cw', units.usDelay)

            elif (dif_x == -2) and (dif_y == 1):
                motorY.step((travelFieldsY / 2), 'cw', units.usDelay)
                motorX.step(travelFieldsX, 'ccw', units.usDelay)
                motorY.step((travelFieldsY / 2), 'cw', units.usDelay)

            elif (dif_x == -1) and (dif_y == 2):
                motorX.step((travelFieldsX / 2), 'ccw', units.usDelay)
                motorY.step(travelFieldsY, 'cw', units.usDelay)
                motorX.step((travelFieldsX / 2), 'ccw', units.usDelay)

            elif (dif_x == 2) and (dif_y == -1):
                motorY.step((travelFieldsY / 2), 'ccw', units.usDelay)
                motorX.step(travelFieldsX, 'cw', units.usDelay)
                motorY.step((travelFieldsY / 2), 'ccw', units.usDelay)

            elif (dif_x == 1) and (dif_y == -2):
                motorX.step((travelFieldsX / 2), 'cw', units.usDelay)
                motorY.step(travelFieldsY, 'ccw', units.usDelay)
                motorX.step((travelFieldsX / 2), 'cw', units.usDelay)

            elif (dif_x == -2) and (dif_y == -1):
                motorY.step((travelFieldsY / 2), 'ccw', units.usDelay)
                motorX.step(travelFieldsX, 'ccw', units.usDelay)
                motorY.step((travelFieldsY / 2), 'ccw', units.usDelay)

            elif (dif_x == -1) and (dif_y == -2):
                motorX.step((travelFieldsX / 2), 'ccw', units.usDelay)
                motorY.step(travelFieldsY, 'ccw', units.usDelay)
                motorX.step((travelFieldsX / 2), 'ccw', units.usDelay)
                
            else: 
                # Non-Knight Movement
                if dif_x > 0:
<<<<<<< HEAD
                    motorX.step(travelFieldsX, 'cw', units.usDelay)

                elif dif_x < 0:
                    motorX.step(travelFieldsX, 'ccw', units.usDelay)

                if dif_y > 0:
                    motorY.step(travelFieldsY, 'cw', units.usDelay)

                elif dif_y < 0:
                    motorY.step(travelFieldsY, 'ccw', units.usDelay)
=======
                    travelFields = units.fieldSteps * dif_x
                    def motorStepXPos():
                        motorX.step(travelFields, 'cw', units.usDelay)
                    Thread(target = motorStepXPos).start()

                elif dif_x < 0:
                    travelFields = units.fieldSteps * dif_x * -1
                    def motorStepXNeg():
                        motorX.step(travelFields, 'ccw', units.usDelay)
                    Thread(target = motorStepXNeg).start()
                    motorX.step(travelFieldsX, 'ccw', units.usDelay)

                if dif_y > 0:
                    travelFields = units.fieldSteps * dif_y
                    def motorStepYPos():
                        motorY.step(travelFields, 'cw', units.usDelay)
                    Thread(target = motorStepYPos).start()
                    motorY.step(travelFieldsY, 'cw', units.usDelay)

                elif dif_y < 0:
                    travelFields = units.fieldSteps * dif_y * -1
                    def motorStepYNeg():
                        motorY.step(travelFields, 'ccw', units.usDelay)
                    Thread(target = motorStepYNeg).start()
>>>>>>> 00d382c410b568bd56ebc0b0997a1c7b13986c60

        except KeyboardInterrupt:
            GPIO.output(motorX.EN, GPIO.HIGH)
            GPIO.output(motorY.EN, GPIO.HIGH)

    def manual_movement():
        move_x = int(input("Move fields in X direction: "))
        move_y = int(input("Move fields in Y direciton: "))

        Motor_move.move_motor_on_board(move_x, move_y, units)

Motor_move.manual_movement()


# def moveX():
#     motorX.step((units.fieldSteps * 6), 'cw', units.usDelay)

# def moveY():
#     motorY.step((units.fieldSteps * 6), 'ccw', units.usDelay)

# def moveXback():
#     motorX.step((units.fieldSteps * 5), 'ccw', units.usDelay)

# def moveYback():
#     motorY.step((units.fieldSteps * 5), 'ccw', units.usDelay)

# def move():
#     Thread(target = moveX).start()
#     Thread(target = moveY).start()

# def moveback():
#     Thread(target = moveXback).start()
#     Thread(target = moveYback).start()
# move()
# moveback()