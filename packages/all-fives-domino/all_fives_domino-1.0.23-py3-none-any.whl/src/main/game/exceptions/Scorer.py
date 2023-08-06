class ScoringException(Exception):
    pass


class ScoringRecursionException(ScoringException):
    def __init__(self, message: str, board: "Board" = None):
        super().__init__(message)
        self.board = board
