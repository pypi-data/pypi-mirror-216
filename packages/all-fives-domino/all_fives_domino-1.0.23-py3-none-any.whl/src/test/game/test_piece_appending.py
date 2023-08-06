from src.main.game.Piece import Piece


def test_append_sequence():
    p55 = Piece(5, 5)
    p52 = Piece(5, 2)

    p55.append(p52)

    assert p52.linked_to == p55
    assert p52.linked == []
    assert p55.linked_to is None
    assert p55.linked == [p52]
