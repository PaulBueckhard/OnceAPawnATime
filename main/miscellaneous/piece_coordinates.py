class ChessPiece:
    def __init__(self, from_x, from_y, to_x, to_y, current_position_x, current_position_y, difference_from_to, difference_current_from, player_move, ai_move, ai_from, ai_to):
        self.from_x = from_x
        self.from_y = from_y

        self.to_x = to_x
        self.to_y = to_y

        self.current_position_x = current_position_x
        self.current_position_y = current_position_y

        self.difference_from_to = difference_from_to
        self.difference_current_from = difference_current_from

        self.player_move = player_move

        self.ai_move = ai_move
        self.ai_from = ai_from
        self.ai_to = ai_to
    
    def coordinate_converter_robot(self, from_pos, to_pos):
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

    def coordinate_converter_ai(self, from_pos, to_pos):
        self.player_move = from_pos + to_pos
        self.player_move = self.player_move.lower()
        return self.player_move
    
    def coordinate_converter_webserver(self, ai_move):
        ai_move = str(ai_move)
        ai_move = ai_move.upper()
        ai_from, ai_to = ai_move[:len(ai_move)//2], ai_move[len(ai_move)//2:]
        self.ai_from = ai_from
        self.ai_to = ai_to

    def save_current_position(self):
        self.current_position_x = self.to_x
        self.current_position_y = self.to_y

    def calculate_difference_from_to(self):
        dif_x = self.to_x - self.from_x
        dif_y = self.to_y - self.from_y
        self.difference_from_to = [dif_x, dif_y]

    def calculate_difference_current_from(self):
        dif_x = self.from_x - self.current_position_x
        dif_y = self.from_y - self.current_position_y
        self.difference_current_from = [dif_x, dif_y]

    def fen_visualiser(self, fen):
        board = []
        for row in fen.split('/'):
            brow = []
            for c in row:
                if c == ' ':
                    break
                elif c in '12345678':
                    brow.extend(['--'] * int(c))
                elif c == 'p':
                    brow.append('♙ ')
                elif c == 'P':
                    brow.append('♟︎ ')
                elif c == 'r':
                    brow.append('♖ ')
                elif c == 'R':
                    brow.append('♜ ')
                elif c == 'n':
                    brow.append('♘ ')
                elif c == 'N':
                    brow.append('♞ ')
                elif c == 'b':
                    brow.append('♗ ')
                elif c == 'B':
                    brow.append('♝ ')
                elif c == 'q':
                    brow.append('♕ ')
                elif c == 'Q':
                    brow.append('♛ ')
                elif c == 'k':
                    brow.append('♔ ')
                elif c == 'K':
                    brow.append('♚ ')

            board.append(brow)
        return board
