class GameWinSignal(Exception):
    """Raised when a player wins to stop the game"""
    def __init__(self, winner: "Player"):
        super().__init__(f"{winner.name} wins!")
        self.winner = winner
