import uuid
from typing import Union

from src.main.game.Game import Game
from src.main.server.exceptions.Lobby import LobbyStartException


class Lobby:
    def __init__(self):
        self.players = []
        self.game: Union[Game, None] = None
        self.uuid = uuid.uuid4()

    def start(self):
        if len(self.players) < 2:
            raise LobbyStartException(f"Two players are required to start Lobby {self.uuid}")

        self.game = Game(self.players[0], self.players[1], interactive=True)
        self.game.run()
