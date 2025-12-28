from boto.dynamodb2.layer1 import DynamoDBConnection
from boto.dynamodb2.fields import HashKey, RangeKey, GlobalAllIndex
from boto.dynamodb2.table import Table
from boto.exception import JSONResponseError

def getDynamoDBConnection(endpoint=None, local=False, **kwargs):
    if local:
        return DynamoDBConnection(
            host=endpoint,
            port=8000,
            aws_access_key_id="dummy",
            aws_secret_access_key="dummy",
            is_secure=False
        )
    return DynamoDBConnection(is_secure=True)

def createGamesTable(db):
    try:
        return Table.create(
            "Games",
            schema=[HashKey("GameId")],
            global_indexes=[
                GlobalAllIndex(
                    "HostId-StatusDate-index",
                    parts=[HashKey("HostId"), RangeKey("StatusDate")]
                ),
                GlobalAllIndex(
                    "OpponentId-StatusDate-index",
                    parts=[HashKey("OpponentId"), RangeKey("StatusDate")]
                ),
            ],
            throughput={"read": 1, "write": 1},
            connection=db
        )
    except JSONResponseError:
        return Table("Games", connection=db)
