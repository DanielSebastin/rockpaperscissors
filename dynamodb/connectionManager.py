from .setupDynamoDB import getDynamoDBConnection, createGamesTable
from boto.dynamodb2.table import Table

class ConnectionManager:
    def __init__(self, mode="service"):
        if mode == "local":
            self.db = getDynamoDBConnection(endpoint="localhost", local=True)
        else:
            self.db = getDynamoDBConnection()

        self.gamesTable = Table("Games", connection=self.db)

    def getGamesTable(self):
        return self.gamesTable

    def createGamesTable(self):
        self.gamesTable = createGamesTable(self.db)
