import pytest

from src.main.game.Board import Board
from src.main.game.Piece import Piece
from src.main.game.exceptions.Board import DuplicatePieceException


def test_find_piece():
    board = Board()
    p55 = Piece(5, 5)
    p52 = Piece(5, 2)
    p54 = Piece(5, 4)

    board.play(p55)
    board.play(p52, p55)

    assert board.find_piece([5, 5]) is not None
    assert board.find_piece([5, 2]) is not None
    assert board.find_piece([1, 2]) is None
    assert board.find_piece([5, 4]) is None

    board.play(p54, p55)

    assert board.find_piece([5, 4]) is not None


def test_board_duplicate():
    board = Board()
    p55 = Piece(5, 5)
    p52 = Piece(5, 2)
    p54 = Piece(5, 4)

    board.play(p55)
    board.play(p52, p55)
    board.play(p54, p55)

    with pytest.raises(DuplicatePieceException):
        p54_2 = Piece(5, 4)
        board.play(p54_2, p55)

    with pytest.raises(DuplicatePieceException):
        board.play(p54, p55)
