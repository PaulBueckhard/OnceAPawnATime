class Pins:
    def __init__(self, motorId):
        print(f"Setting pins for {motorId}.")
        self.STEP = 2 # Step GPIO pin
        self.DIR = 3 # Direction GPIO pin
        self.EN = 4 # Enable pin