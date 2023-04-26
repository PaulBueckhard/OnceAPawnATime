import chess
from ..main.chess_ai.chess_ai import ChessAI

board = chess.Board()

# Test evaluate board function
def test_initial_position():
    assert ChessAI.evaluate_board(board) == 0

def test_scoring_for_material():
    board.set_fen("8/8/8/8/8/8/8/rnbqkbnr w KQkq - 0 1")
    assert ChessAI.evaluate_board(board) == 31

def test_scoring_for_control():
    board.set_fen("8/8/8/8/4P3/8/8/8 w - - 0 1")
    assert ChessAI.evaluate_board(board) == -1

def test_scoring_for_checkmate():
    board.set_fen("8/8/8/8/8/8/2k5/R7 w - - 0 1")
    assert ChessAI.evaluate_board(board) == -5

# Test minimax function
def test_empty_board():
    board = chess.Board()
    assert ChessAI.minimax(board, 3, float('-inf'), float('inf'), True) == 0

def test_starting_position_depth_1():
    assert ChessAI.minimax(board, 1, float('-inf'), float('inf'), True) != None

def test_only_pawns():
    board = chess.Board('8/8/8/8/8/8/PPPPPPPP/8 w - - 0 1')
    assert ChessAI.minimax(board, 3, float('-inf'), float('inf'), True) == -8

def test_forced_checkmate_in_3_moves():
    board.set_fen("3qk3/8/8/8/8/8/8/R3K2R w KQ - 0 1")
    assert ChessAI.minimax(board, 3, float('-inf'), float('inf'), True) == -1

def test_board_is_checkmate():
    board = chess.Board('rnbqkbnr/pppp1ppp/8/4p3/2B1P3/8/PPPP1PPP/RNBQK1NR b KQkq - 1 2')
    assert ChessAI.minimax(board, 3, float('-inf'), float('inf'), True) == 1

def test_board_is_stalemate():
    board = chess.Board('k7/8/Q7/8/8/8/8/K7 b - - 0 1')
    assert ChessAI.minimax(board, 4, float('-inf'), float('inf'), True) == -9

def test_forced_draw():
    board.set_fen("8/8/8/8/8/8/6k1/6qk w - - 0 1")
    assert ChessAI.minimax(board, 3, float('-inf'), float('inf'), True) == 9

def test_ai_wins_piece():
    board.set_fen("8/8/8/8/2k5/8/5B2/8 w - - 0 1")
    assert ChessAI.minimax(board, 3, float('-inf'), float('inf'), True) == -3

def test_white_winning():
    board = chess.Board('rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1')
    assert ChessAI.minimax(board, 5, float('-inf'), float('inf'), True) > 0

def test_black_winning():
    board = chess.Board('rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1')
    assert ChessAI.minimax(board, 5, float('-inf'), float('inf'), False) < 0

# Test function correctness
def test_function_does_not_modify_input_board():
    board = chess.Board('rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1')
    board_copy = board.copy()
    ChessAI.minimax(board, 4, float('-inf'), float('inf'), True)
    assert board == board_copy

def test_function_returns_same_value_regardless_of_order():
    board = chess.Board('rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1')
    eval1 = ChessAI.minimax(board, 4, float('-inf'), float('inf'), True)

    board_copy = board.copy()
    eval2 = ChessAI.minimax(board_copy, 4, float('-inf'), float('inf'), True)

    assert eval1 == eval2
