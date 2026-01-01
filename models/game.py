class Game:
    def __init__(self,item):
        self.gameId=item["GameId"]
        self.hostId=item["HostId"]
        self.opponentId=item["OpponentId"]
        self.hostChoice=item.get("HostChoice")
        self.opponentChoice=item.get("OpponentChoice")
        self.result=item.get("Result")

    def getOpposingPlayer(self,user):
        return self.opponentId if user==self.hostId else self.hostId

    def getPlayerChoice(self,user):
        if user==self.hostId:
            return self.hostChoice
        if user==self.opponentId:
            return self.opponentChoice
        return None

    def getResult(self,user):
        if not self.result:
            return None
        if self.result=="Tie":
            return "Tie"
        return "Win" if self.result==user else "Lose"
