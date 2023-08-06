from typing import Union, List

from src.main.game.Piece import Piece

from src.main.game.exceptions.Board import InvalidCloseException, InvalidMoveException, DuplicatePieceException


class Board:
    def __init__(self):
        self.origin: Union[Piece, None] = None
        self.has_crossing = False

    def json(self):
        return {
            "origin": self.origin.json(),
            "hasCrossing": self.has_crossing
        }

    def play(self, piece: Piece, origin: Union[Piece, None] = None, close = False):
        if self.find_piece(piece.sides):
            raise DuplicatePieceException(f"Attempted to play {piece}, but it is already on the board", self)

        if origin is not None:
            origin = self.find_piece(origin.sides)
            if origin is None:
                raise InvalidMoveException(f"Attempted to append on {origin}, but it's not on the board", self)

        if close:
            if not piece.is_double:
                raise InvalidCloseException(f"Cannot play {piece} closed: Not a double piece", self)

            if not self.has_crossing:
                raise InvalidCloseException(f"Cannot play a closed piece while there is no cross piece", self)

            piece.closed = True

        if origin is None:
            if self.origin is not None:
                raise InvalidMoveException(f"Player attempted to play {piece} as origin, "
                                           f"but board already has origin piece {self.origin}", self)
            self.origin = piece
        else:
            origin.append(piece)

        if self.has_crossing and origin is not None:
            origin.is_crossing = False
        else:
            if origin is not None and origin.is_crossing:
                self.has_crossing = True

    def open_ends(self, piece: Piece = None):
        # Default to origin piece
        piece = piece or self.origin

        ends = [(piece, side) for side in piece.open_sides]
        for linked_piece in piece.linked:
            ends += self.open_ends(linked_piece)

        return sorted(ends)

    def get_pieces(self, piece: Piece = None):
        # Default to origin piece
        piece = piece or self.origin

        # If piece is None, the board is empty (since origin is None)
        if piece is None:
            return []

        pieces = [piece]
        for linked_piece in piece.linked:
            pieces += self.get_pieces(linked_piece)
        return pieces

    def find_piece(self, sides: List[int]):
        """Find a piece by its sides on the board"""
        a, b = sides
        compare_piece = Piece(a, b)
        for piece in self.get_pieces():
            if piece == compare_piece:
                return piece
