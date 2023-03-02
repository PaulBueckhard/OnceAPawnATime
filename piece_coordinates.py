class ChessPiece:
    def __init__(self, from_x, from_y, to_x, to_y, difference):
        self.from_x = from_x
        self.from_y = from_y
        self.to_x = to_x
        self.to_y = to_y
        self.difference = difference
    
    def coordinate_converter(self, from_pos, to_pos):
        coordinates = []
        coordinates[:0] = from_pos + to_pos

        for i in range(len(coordinates)):
            if coordinates[i] == "A":
                coordinates[i] = 1

            elif coordinates[i] == "B":
                coordinates[i] = 2

            elif coordinates[i] == "C":
                coordinates[i] = 3

            elif coordinates[i] == "D":
                coordinates[i] = 4

            elif coordinates[i] == "E":
                coordinates[i] = 5

            elif coordinates[i] == "F":
                coordinates[i] = 6

            elif coordinates[i] == "G":
                coordinates[i] = 7

            elif coordinates[i] == "H":
                coordinates[i] = 8

        coordinates = [int(x) for x in coordinates]
        
        self.from_x = coordinates[0]
        self.from_y = coordinates[1]
        self.to_x = coordinates[2]
        self.to_y = coordinates[3]

    def calculate_difference(self):
        dif_x = self.to_x - self.from_x
        dif_y = self.to_y - self.from_y
        self.difference = [dif_x, dif_y]
