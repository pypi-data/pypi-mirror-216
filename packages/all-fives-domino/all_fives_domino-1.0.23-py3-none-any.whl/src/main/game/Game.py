import uuid

from src.main.game.DominoRound import DominoRound
from src.main.game.Player import Player

from src.main.game.exceptions.Game import GameWinSignal


class GameStatus:
    WAITING = "Waiting"
    RUNNING = "Running"
    OVER = "Over"
    INTERRUPTED = "Interrupted"


class Game:
    def __init__(self, player1: Player, player2: Player, interactive=False):
        self.target_score = 305
        self.eggs = 0
        self.rounds = 0
        self.player1 = player1
        self.player2 = player2
        self.status = GameStatus.WAITING
        self.round: DominoRound = None
        self.interactive = interactive
        self.id = uuid.uuid4()

    def json(self):
        return {
            "targetScore": self.target_score,
            "eggs": self.eggs,
            "rounds": self.rounds,
            "player1": self.player1.json(),
            "player2": self.player2.json(),
            "status": self.status,
            "round": None if self.round is None else self.round.json()
        }

    def run(self):
        self.status = GameStatus.RUNNING
        try:
            while self.rounds < 1000 and self.status == GameStatus.RUNNING:
                self.rounds += 1
                self.round = DominoRound(self.player1, self.player2, self)
                self.round.run()
                self.award_round_score()
        except GameWinSignal as win_signal:
            print(win_signal)

        self.status = GameStatus.OVER

    def award_round_score(self):
        player1_score = sum([piece.points for piece in self.player1.hand])
        player2_score = sum([piece.points for piece in self.player2.hand])

        if player1_score == player2_score:
            self.eggs += player1_score + player2_score
        elif player1_score < player2_score:
            self.player1.score += player2_score + self.eggs
            self.eggs = 0
        else:
            self.player2.score += player1_score + self.eggs
            self.eggs = 0
