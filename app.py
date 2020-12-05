from flask import Flask, request, render_template, jsonify, session
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.route("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.route("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    info = {"gameId": game_id, "board": games[game_id].board}

    return jsonify(info)
    # return {"gameId": "need-real-id", "board": "need-real-board"}


@app.route("/api/score-word", methods=['POST'])
def score_word():
    """ accepts POST rqst w/ JSON for gameId and word
        checks if word is legal:
            in word list
            findable on board
        returns JSON response

    """
   
    word = request.json['word'].upper()
    gameid = request.json['gameId']

    breakpoint()

    current_game = games[gameid]

    if not current_game.is_word_in_word_list(word):
        return jsonify({'result': "not-word"})
    elif not current_game.check_word_on_board(word):
        return jsonify({'result': "not-on-board"})
    else:
        return jsonify({'result': "ok"})
   


