class BoardException(Exception):
    def __init__(self, message: str, board: "Board" = None):
        super().__init__(message)
        self.board = board


class InvalidMoveException(Exception):
    pass


class InvalidCloseException(InvalidMoveException):
    pass


class DuplicatePieceException(InvalidMoveException):
    pass