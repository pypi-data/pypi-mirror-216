from typing import List, Union

from src.main.server.Lobby import Lobby
from src.main.game.Game import Game


class LobbyManager:
    def __init__(self):
        self.lobbies: List[Lobby] = []

    def create_lobby(self):
        self.lobbies.append(Lobby())

    def get_lobby(self, uuid: str):
        for lobby in self.lobbies:
            if lobby.uuid == uuid or (lobby.game is not None and lobby.game.uuid == uuid):
                return lobby

    def get_game(self, uuid: str) -> Union[Game, None]:
        for lobby in self.lobbies:
            if lobby.game is not None and lobby.game.uuid == uuid:
                return lobby.game
