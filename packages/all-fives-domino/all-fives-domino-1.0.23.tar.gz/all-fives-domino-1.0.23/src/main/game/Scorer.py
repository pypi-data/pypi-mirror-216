from src.main.game.exceptions.Scorer import ScoringRecursionException


class Scorer:
    @classmethod
    def count(cls, piece: "Piece", depth=28) -> int:
        """Calculate the current point value for a board by its origin piece"""
        raise NotImplementedError("No counting method, override this!")

    @classmethod
    def score(cls, count: int) -> int:
        """Calculate the score that should be awarded for a board state"""
        raise NotImplementedError("No scoring method, override this!")

    @classmethod
    def board_score(cls, board: "Board") -> int:
        return cls.score(cls.count(board.origin))


class AllFivesScorer(Scorer):
    @classmethod
    def count(cls, piece: "Piece", depth=28) -> int:
        # Contingency against loops
        if depth < 0:
            raise ScoringRecursionException("Recursion too deep, some pieces linked in a loop?")

        score = 0

        # If no pieces are attached, the score is the value of the piece
        if piece.closed_sides == 0:
            score += piece.points

        # If one of the sides is an end, the score is that side. For doubles, both sides are counted
        if piece.closed_sides == 1:
            if piece.is_double:
                score += piece.points
            else:
                score += sum(piece.open_sides)

        # For crossing pieces with exactly 3 connections, the open side is also counted
        if piece.is_crossing and piece.closed_sides == 3:
            score += piece.sides[0]

        # Score all connected pieces
        for linked_piece in piece.linked:
            score += cls.count(linked_piece, depth - 1)

        return score

    @classmethod
    def score(cls, count: int) -> int:
        return count if (count % 5 == 0) else 0
