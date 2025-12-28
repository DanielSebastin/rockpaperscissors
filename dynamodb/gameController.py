from boto.dynamodb2.exceptions import ConditionalCheckFailedException
from boto.dynamodb2.items import Item
from datetime import datetime

class GameController:
    def __init__(self, cm):
        self.cm = cm

    def createNewGame(self, gameId, host, opponent):
        item = Item(self.cm.getGamesTable(), data={
            "GameId": gameId,
            "HostId": host,
            "OpponentId": opponent,
            "StatusDate": "IN_PROGRESS_" + str(datetime.now()),
            "HostChoice": None,
            "OpponentChoice": None,
            "Result": None
        })
        return item.save()

    def getGame(self, gameId):
        try:
            return self.cm.getGamesTable().get_item(GameId=gameId)
        except:
            return None

    def submitChoice(self, game, user, choice):
        field = "HostChoice" if user == game["HostId"] else "OpponentChoice"
        try:
            self.cm.db.update_item(
                "Games",
                key={"GameId": {"S": game["GameId"]}},
                attribute_updates={
                    field: {"Action": "PUT", "Value": {"S": choice}}
                },
                expected={field: {"Exists": False}}
            )
            return True
        except ConditionalCheckFailedException:
            return False

    def resolveGame(self, game):
        h, o = game.get("HostChoice"), game.get("OpponentChoice")
        if not h or not o:
            return

        if h == o:
            result = "Tie"
        elif (h, o) in [("ROCK","SCISSORS"),("PAPER","ROCK"),("SCISSORS","PAPER")]:
            result = game["HostId"]
        else:
            result = game["OpponentId"]

        game["Result"] = result
        game["StatusDate"] = "FINISHED_" + str(datetime.now())
        game.save()
