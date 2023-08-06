from src.main.game.DominoRound import DominoRound
from src.main.game.Brain import AllFivesGreedyBrain, RandomBrain
from src.main.game.Player import Player
from src.main.game.Game import Game
from src.main.game.Piece import Piece


def test_round_initialization():
    # Initialize a round and check there's a valid starting setup
    game = Game(Player(RandomBrain()), Player(RandomBrain()))
    round = DominoRound(Player(RandomBrain()), Player(RandomBrain()), game)

    assert round.board.origin is not None
    assert round.board.origin.is_double


def assert_options(round, plays):
    options = round.valid_options()

    assert len(options) == len(plays)

    for piece, origin, closed in plays:
        assert any([piece == o_piece.sides and origin == o_origin.sides and closed == o_closed for o_piece, o_origin, o_closed in options])


def test_options_calculation():
    # Check that options are determined correctly
    game = Game(Player(RandomBrain()), Player(RandomBrain()))
    round = DominoRound(Player(RandomBrain()), Player(RandomBrain()), game)

    """Test appending to [3|3] starting Piece"""

    round.board.origin = Piece(3, 3)

    round.current_player.hand.pieces = [Piece(3, 2), Piece(3, 1), Piece(1, 1), Piece(1, 2)]
    assert_options(round, [
        ([2, 3], [3, 3], False),
        ([1, 3], [3, 3], False)
    ])

    round.board.origin.append(Piece(3, 4))
    round.board.origin.append(Piece(3, 5))

    assert_options(round, [
        ([2, 3], [3, 3], False),
        ([1, 3], [3, 3], False)
    ])

    """Test appending to double corner Piece"""

    round.board.origin = Piece(2, 2)
    round.board.origin.append(Piece(2, 0))
    round.board.origin.append(Piece(2, 5))
    round.board.origin.linked[1].append(Piece(5, 6))
    round.board.origin.linked[0].append(Piece(0, 0))

    round.current_player.hand.pieces = [Piece(3, 2), Piece(0, 1), Piece(0, 6), Piece(4, 5)]
    assert_options(round, [
        ([2, 3], [2, 2], False),
        ([0, 1], [0, 0], False),
        ([0, 6], [0, 0], False),
        ([0, 6], [5, 6], False)
    ])
