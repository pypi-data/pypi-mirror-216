from typing import List

from src.main.game.Piece import Piece
from src.main.game.exceptions.Hand import HandDuplicateException


class Hand:
    def __init__(self, *pieces: Piece):
        self.pieces: List[Piece] = list(pieces)
        self.validate()

    def add(self, piece: Piece):
        self.pieces.append(piece)
        self.validate()

    def pop(self, piece: Piece):
        self.pieces = [p for p in self.pieces if p != piece]
        self.validate()
        return piece

    def check_duplicates(self):
        for piece in self.pieces:
            if self.pieces.count(piece) > 1:
                raise HandDuplicateException(f"{piece} contained in hand {self.pieces.count(piece)} times", self)

    def validate(self):
        self.order()
        self.check_duplicates()

    def order(self):
        self.pieces.sort()

    def __iter__(self):
        for piece in self.pieces:
            yield piece

    def __len__(self):
        return len(self.pieces)

    def __repr__(self):
        return repr(self.pieces)

    def json(self):
        return [piece.json() for piece in self.pieces]
