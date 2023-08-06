from flask import Flask, send_from_directory, abort
from flask_socketio import SocketIO, join_room, leave_room, send, emit

from src.main.game.Game import Game, GameStatus
from src.main.game.Brain import AllFivesGreedyBrain, PlayerBrain
from src.main.server.LobbyManager import LobbyManager

app = Flask(__name__)
socketio = SocketIO(app)
lobby_manager = LobbyManager()


@app.route("/")
def get_home():
    return send_from_directory("static", "index.html")


@app.route("/lobby")
def get_lobby():
    return send_from_directory("static", "lobby.html")


@app.route("/game")
def get_game():
    return send_from_directory("static", "game.html")


@app.route("/status/<game_uuid>")
def get_status(game_uuid: str):
    game = lobby_manager.get_game(game_uuid)

    if game is None:
        abort(404, description=f"Game {game_uuid} not found")

    return game.json()


@app.route("/start/<lobby_uuid>")
async def start_game(lobby_uuid: str):
    lobby = lobby_manager.get_lobby(lobby_uuid)

    if lobby is None:
        abort(404, description=f"Lobby {lobby_uuid} not found")

    lobby.run()
    return "OK"


@app.route("/play/<game_uuid>/<option>")
def player_decision(game_uuid: str, option: str):
    game = lobby_manager.get_game(game_uuid)

    if game is None:
        abort(404, description=f"Game {game_uuid} not found")

    if not isinstance(game.round.current_player.brain, PlayerBrain):
        abort(400, description="Not the player's turn")

    game.round.current_player.brain.decision = int(option)
    return "OK"


@socketio.event
def join(data):
    print(data)


@socketio.event
def leave(data):
    print(data)


@socketio.event
def connect(data):
    pass


if __name__ == '__main__':
    socketio.run(app)
