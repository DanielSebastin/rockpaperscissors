from flask import Flask, render_template, request, redirect, session
from uuid import uuid4
from dynamodb.connectionManager import ConnectionManager
from dynamodb.gameController import GameController
from models.game import Game

app = Flask(__name__)
app.secret_key = "rps-secret"

cm = ConnectionManager()
controller = GameController(cm)

@app.route("/",methods=["GET","POST"])
def index():
    if request.method=="POST":
        session["user"]=request.form["username"]
    return render_template("index.html",user=session.get("user"))

@app.route("/create",methods=["POST"])
def create():
    gid=str(uuid4())
    controller.create_game(
        gameId=gid,
        host=session["user"],
        opponent=request.form["opponent"]
    )
    return redirect(f"/game/{gid}")

@app.route("/game/<gid>")
def game(gid):
    item=controller.get_game(gid)
    if not item:
        return "Game not found",404

    g=Game(item)

    return render_template(
        "play.html",
        game=g,
        user=session["user"],
        myChoice=g.getPlayerChoice(session["user"]),
        opponent=g.getOpposingPlayer(session["user"]),
        opponentChoice=g.getPlayerChoice(g.getOpposingPlayer(session["user"])),
        result=g.getResult(session["user"])
    )

@app.route("/choose/<gid>",methods=["POST"])
def choose(gid):
    controller.submit_choice(
        gid,
        user=session["user"],
        choice=request.form["choice"]
    )
    return redirect(f"/game/{gid}")

if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0",port=5000)
