import chess
import random

# A simple evaluation function that counts the total value of each player's pieces on the board
def evaluate_board(board):
    piece_values = {"P": 1, "N": 3, "B": 3, "R": 5, "Q": 9, "K": 0}
    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            value = piece_values[piece.symbol().upper()]
            if piece.color == chess.WHITE:
                score += value
            else:
                score -= value
    return score

# A simple minimax algorithm with alpha-beta pruning
def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if maximizing_player:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# A function that chooses a random legal move
def random_move(board):
    legal_moves = list(board.legal_moves)
    return random.choice(legal_moves)

# The main function that plays a game between the AI and a human player
def play_game():
    board = chess.Board()
    while not board.is_game_over():
        if board.turn == chess.WHITE:
            # The AI plays as the black player
            move = None
            max_eval = float('-inf')
            for possible_move in board.legal_moves:
                board.push(possible_move)
                eval = minimax(board, 3, float('-inf'), float('inf'), False)
                board.pop()
                if eval > max_eval:
                    max_eval = eval
                    move = possible_move
            board.push(move)
            print(f"AI played {move}")
        else:
            # The human player plays as the white player
            move = None
            while move not in board.legal_moves:
                move_string = input("Enter your move (in algebraic notation): ")
                move = chess.Move.from_uci(move_string)
            board.push(move)
        print(board)

    # Print the result of the game
    if board.result() == "1-0":
        print("White wins!")
    elif board.result() == "0-1":
        print("Black wins!")
    else:
        print("Draw!")

# Play a game
play_game()
