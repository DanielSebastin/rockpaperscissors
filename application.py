from flask import Flask, render_template, request, redirect, session
from uuid import uuid4
from dynamodb.connectionManager import ConnectionManager
from dynamodb.gameController import GameController
from models.game import Game

app = Flask(__name__)
app.secret_key = "rps-secret"

cm = ConnectionManager(mode="local")  # change to "service" on EC2
controller = GameController(cm)

@app.route("/", methods=["GET","POST"])
def index():
    if request.form:
        session["user"] = request.form["username"]
    return render_template("index.html", user=session.get("user"))

@app.route("/create", methods=["POST"])
def create():
    gid = str(uuid4())
    controller.createNewGame(gid, session["user"], request.form["opponent"])
    return redirect(f"/game/{gid}")

@app.route("/game/<gid>")
def game(gid):
    item = controller.getGame(gid)
    controller.resolveGame(item)
    game = Game(item)
    return render_template("play.html",
        game=game,
        user=session["user"],
        myChoice=game.getPlayerChoice(session["user"]),
        opponent=game.getOpposingPlayer(session["user"]),
        opponentChoice=game.getPlayerChoice(game.getOpposingPlayer(session["user"])),
        result=game.getResult(session["user"])
    )

@app.route("/choose/<gid>", methods=["POST"])
def choose(gid):
    controller.submitChoice(
        controller.getGame(gid),
        session["user"],
        request.form["choice"]
    )
    return redirect(f"/game/{gid}")

app.run(debug=True)
