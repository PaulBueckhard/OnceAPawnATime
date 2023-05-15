class Units:
    # 2400 steps makes about 46.5 cm linear distance (5.1613 steps/mm)
    MIN_US_DELAY = 950
    usDelay = 950 # number of microseconds
    uS = 0.000001 # one microsecond
    spmm = 5.1613 # steps/mm
    fieldLength = 58 # width and length of a field on the board in mm
    # clockwise movement on motor_x is X positive
    # counterclockwise movement on motor_x is X negative
    fieldSteps = 299 # One fieldlength in steps