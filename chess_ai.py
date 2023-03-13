import chess
import random

class ChessAI:

    def evaluate_board(board):
        piece_values = {"P": 1, "N": 3, "B": 3, "R": 5, "Q": 9, "K": 0}
        score = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                value = piece_values[piece.symbol().upper()]
                if piece.color == chess.BLACK:
                    score += value
                else:
                    score -= value
        return score

    def minimax(board, depth, alpha, beta, maximizing_player):
        if depth == 0 or board.is_game_over():
            return ChessAI.evaluate_board(board)

        if maximizing_player:
            max_eval = float('-inf')
            for move in board.legal_moves:
                board.push(move)
                eval = ChessAI.minimax(board, depth - 1, alpha, beta, False)
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
                eval = ChessAI.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def random_move(board):
        legal_moves = list(board.legal_moves)
        return random.choice(legal_moves)
