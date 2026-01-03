from utils import decide_winner
from datetime import datetime


class GameController:
    def __init__(self,connection_manager):
        self.cm=connection_manager
        self.table=self.cm.get_table()

    def create_game(self,game_id,host_id,opponent_id):
        self.table.put_item(
            data={
                "GameId":game_id,
                "HostId":host_id,
                "OpponentId":opponent_id,
                "HostChoice":None,
                "OpponentChoice":None,
                "Status":"WAITING",
                "Result":None,
                "CreatedAt":str(datetime.utcnow())
            }
        )

    def get_game(self,game_id):
        return self.table.get_item(GameId=game_id)


    def accept_game(self,game_id):
        game=self.get_game(game_id)
        game["Status"]="ACTIVE"
        game.save()

    def reject_game(self,game_id):
        game=self.get_game(game_id)
        game["Status"]="REJECTED"
        game.save()

    def submit_choice(self,game_id,player_id,choice):
        game=self.get_game(game_id)

        if game["Status"]!="ACTIVE":
            return

        if game["HostId"]==player_id:
            game["HostChoice"]=choice
        elif game["OpponentId"]==player_id:
            game["OpponentChoice"]=choice
        else:
            return

        if game["HostChoice"] and game["OpponentChoice"]:
            result=decide_winner(game["HostChoice"],game["OpponentChoice"])
            game["Result"]=result
            game["Status"]="FINISHED"

        game.save()
