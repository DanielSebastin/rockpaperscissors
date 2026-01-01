import boto3

def create_games_table():
    dynamodb=boto3.client("dynamodb",region_name="ap-south-1")

    existing=dynamodb.list_tables()["TableNames"]
    if "Games" in existing:
        print("Table already exists.")
        return

    dynamodb.create_table(
        TableName="Games",
        KeySchema=[
            {"AttributeName":"GameId","KeyType":"HASH"}
        ],
        AttributeDefinitions=[
            {"AttributeName":"GameId","AttributeType":"S"}
        ],
        BillingMode="PAY_PER_REQUEST"
    )

    print("Games table created.")
