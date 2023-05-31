class Pins:
    def __init__(self, motorId):
        # print(f"Setting pins for {motorId}.")
        self.STEP_X = 2 # Step GPIO pin
        self.DIR_X = 17 # Direction GPIO pin
        self.EN_X = 4 # Enable pin

        self.STEP_Y = 0 # Step GPIO pin
        self.DIR_Y = 5 # Direction GPIO pin
        self.EN_Y = 6 # Enable pin