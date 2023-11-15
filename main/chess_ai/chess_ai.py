import chess

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

    def play_move(chesspiece, board, depth, move_from, move_to):
        chesspiece.coordinate_converter_ai(move_from, move_to)
        player_move = chesspiece.player_move
        
        move = None
        while move not in board.legal_moves:
            move = chess.Move.from_uci(player_move)
        board.push(move)

        move = None
        max_eval = float('-inf')
        for possible_move in board.legal_moves:
            board.push(possible_move)
            eval = ChessAI.minimax(board, depth, float('-inf'), float('inf'), False)
            board.pop()
            if eval > max_eval:
                max_eval = eval
                move = possible_move
        board.push(move)
        chesspiece.coordinate_converter_webserver(move)