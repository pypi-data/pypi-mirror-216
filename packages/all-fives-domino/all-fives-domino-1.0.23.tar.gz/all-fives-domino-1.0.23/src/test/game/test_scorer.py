from src.main.game.Scorer import AllFivesScorer
from src.main.game.Piece import Piece


def test_open_double_score():
    board = Piece(5, 5)
    assert AllFivesScorer.count(board) == 10

    board.append(Piece(5, 2))
    assert AllFivesScorer.count(board) == 12

    board.append(Piece(5, 3))
    assert AllFivesScorer.count(board) == 5

    board.append(Piece(5, 0))
    assert AllFivesScorer.count(board) == 10

    board.append(Piece(5, 6))
    assert AllFivesScorer.count(board) == 11
