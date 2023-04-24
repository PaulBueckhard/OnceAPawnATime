
class Pins:
    def __init__(self, motorId):
        print(f"Setting pins for {motorId}.")
        self.STEP = 5 # Step GPIO pin
        self.DIR = 3 # Direction GPIO pin
        self.EN = 23 # Enable pin