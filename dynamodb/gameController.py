import boto3
from datetime import datetime

class GameController:
    def __init__(self,cm):
        self.cm=cm
        self.table=cm.get_table()

    def create_game(self,gameId,host,opponent):
        self.table.put_item(
            Item={
                "GameId":gameId,
                "HostId":host,
                "OpponentId":opponent,
                "HostChoice":None,
                "OpponentChoice":None,
                "Result":None
            }
        )

    def get_game(self,gameId):
        res=self.table.get_item(Key={"GameId":gameId})
        return res.get("Item")

    def submit_choice(self,gameId,user,choice):
        field="HostChoice" if self.get_game(gameId)["HostId"]==user else "OpponentChoice"
        self.table.update_item(
            Key={"GameId":gameId},
            UpdateExpression=f"SET {field}=:c",
            ExpressionAttributeValues={":c":choice}
        )
        self.resolve(gameId)

    def resolve(self,gameId):
        g=self.get_game(gameId)
        h=g.get("HostChoice")
        o=g.get("OpponentChoice")
        if not h or not o:
            return

        if h==o:
            result="Tie"
        elif (h,o) in [("ROCK","SCISSORS"),("PAPER","ROCK"),("SCISSORS","PAPER")]:
            result=g["HostId"]
        else:
            result=g["OpponentId"]

        self.table.update_item(
    Key={'gameId': gameId},
    UpdateExpression="SET #res = :r",
    ExpressionAttributeNames={
        "#res": "Result"
    },
    ExpressionAttributeValues={
        ":r": result
    }
)


