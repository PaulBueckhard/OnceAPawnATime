import chess
from chess_ai import ChessAI

board = chess.Board()

# Test eveluate board function
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
def test_starting_position_depth_1():
    assert ChessAI.minimax(board, 1, float('-inf'), float('inf'), True) != None

def test_position_forced_checkmate_in_3_moves():
    board.set_fen("3qk3/8/8/8/8/8/8/R3K2R w KQ - 0 1")
    assert ChessAI.minimax(board, 3, float('-inf'), float('inf'), True) == -1

def test_position_forced_draw():
    board.set_fen("8/8/8/8/8/8/6k1/6qk w - - 0 1")
    assert ChessAI.minimax(board, 4, float('-inf'), float('inf'), True) == 9

def test_position_ai_wins_piece():
    board.set_fen("8/8/8/8/2k5/8/5B2/8 w - - 0 1")
    assert ChessAI.minimax(board, 2, float('-inf'), float('inf'), True) == -3
