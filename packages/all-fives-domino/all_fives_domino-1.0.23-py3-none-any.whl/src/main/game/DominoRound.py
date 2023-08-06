from typing import Union
import random

from src.main.game.Piece import domino_set, Piece
from src.main.game.Player import Player
from src.main.game.Hand import Hand
from src.main.game.Scorer import AllFivesScorer
from src.main.game.Board import Board


class DominoRound:
    def __init__(self, player1: "Player", player2: "Player", game: "Game", begins: Union["Player", None] = None):
        self.game = game
        self.pool = domino_set()
        random.shuffle(self.pool)
        self.board = Board()

        self.player1 = player1
        self.player2 = player2

        player1.round = self
        player2.round = self

        player1.hand = Hand()
        player2.hand = Hand()

        self.current_player = self.player1 if begins == player1 else (self.player2 if begins == player2 else None)
        self.scorer = AllFivesScorer

        self.start()

    def json(self):
        return {
            "pool": [piece.json() for piece in self.pool],
            "currentPlayer": self.current_player.name,
            "board": self.board.json(),
            "options": [{
                "piece": piece.sides,
                "origin": origin.sides,
                "closed": closed
            } for piece, origin, closed in self.valid_options()]
        }

    def deal_hand(self):
        """Give out 7 initial pieces to each player"""
        for i in range(7):
            self.player1.draw()
            self.player2.draw()

    def check_required_starting_piece(self):
        """
        Find the piece a player is required to start with.

        If no starting player is defined, the player with [5|5] begins.
        If neither player has [5|5], the order goes [1|1], [2|2], ..., [6|6], [0|0].
        If neither player has any double pieces, they draw a piece each until one does.
        """
        if self.current_player is not None:
            return

        piece = None
        while self.current_player is None:
            for i in [5, 1, 2, 3, 4, 6, 0]:
                piece = Piece(i, i)

                if piece in self.player1.hand:
                    self.current_player = self.player1
                    break
                if piece in self.player2.hand:
                    self.current_player = self.player2
                    break

            if self.current_player is None:
                self.player1.draw()
                self.player2.draw()

        self.play(piece)

    def award_score(self):
        """Award any points that are won due to this move"""
        self.current_player.score += self.scorer.board_score(self.board)

    def play(self, piece: Piece, origin: Union[Piece, None] = None, close=False):
        """Play a piece onto the board"""
        player = self.current_player

        if piece not in player.hand:
            raise Exception(f"Player attempted to play {piece}, but it's not in their hand")

        self.board.play(piece, origin, close)
        player.hand.pop(piece)

        self.award_score()
        self.swap_current_player()

    def swap_current_player(self):
        """Change which players turn it is"""
        self.current_player = self.player1 if self.current_player == self.player2 else self.player2

    def valid_options(self, hand: Union[Hand, None] = None):
        """Find all valid moves that can be made in the current board state"""
        hand = hand or self.current_player.hand

        origins = self.board.get_pieces()
        options = []

        for piece in hand:
            for origin in origins:
                if origin.can_append(piece):
                    # Playing the piece open is always an option
                    options.append((piece, origin, False))

                    # If the piece can be played closed, append that option as well
                    if self.board.has_crossing and piece.is_double:
                        options.append((piece, origin, True))

        return options

    def start(self):
        """Initialize the game state"""
        self.deal_hand()
        self.check_required_starting_piece()

    def run(self):
        """Have players take turns until the round ends"""
        while len(self.player1.hand) > 0 and len(self.player2.hand) > 0:
            # If there are no valid options, draw until there is one or there are no pieces left
            while not self.valid_options() and len(self.pool) > 1:
                self.current_player.draw()

            # If still no options, the turn is forfeited
            if not self.valid_options():
                self.swap_current_player()

                # If there are no options for either player, the round is over
                if not self.valid_options():
                    return

            piece, origin, close = self.current_player.brain.decide(self)
            self.play(piece, origin, close)
