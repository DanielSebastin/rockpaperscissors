from flask import Flask,request,jsonify
from connection_manager import ConnectionManager
from game_controller import GameController
from utils import generate_game_id

app=Flask(__name__)

cm=ConnectionManager("config.ini")
gc=GameController(cm)


@app.route("/create-game",methods=["POST"])
def create_game():
    data=request.json
    game_id=generate_game_id()
    gc.create_game(game_id,data["host"],data["opponent"])
    return jsonify({"GameId":game_id})


@app.route("/accept-game",methods=["POST"])
def accept_game():
    data=request.json
    gc.accept_game(data["gameId"])
    return jsonify({"status":"accepted"})


@app.route("/reject-game",methods=["POST"])
def reject_game():
    data=request.json
    gc.reject_game(data["gameId"])
    return jsonify({"status":"rejected"})


@app.route("/submit-choice",methods=["POST"])
def submit_choice():
    data=request.json
    gc.submit_choice(data["gameId"],data["player"],data["choice"])
    return jsonify({"status":"submitted"})


@app.route("/game/<game_id>",methods=["GET"])
def get_game(game_id):
    game=gc.get_game(game_id)
    return jsonify(dict(game))


if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000)
