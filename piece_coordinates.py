class ChessPiece:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def coordinate_converter(string):
        coordinates = []
        coordinates[:0] = string

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
        
        return coordinates


str1 = "B1"
str2 = "C3"
print(ChessPiece.coordinate_converter(str1))
print(ChessPiece.coordinate_converter(str2))
