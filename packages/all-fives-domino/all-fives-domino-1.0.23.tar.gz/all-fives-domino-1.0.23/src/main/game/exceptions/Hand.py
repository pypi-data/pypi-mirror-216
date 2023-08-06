class HandException(Exception):
    def __init__(self, message: str, hand: "Hand" = None):
        super().__init__(message)
        self.hand = hand


class HandDuplicateException(HandException):
    pass
