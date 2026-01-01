import boto3

class ConnectionManager:
    def __init__(self,table_name="Games"):
        self.dynamodb=boto3.resource("dynamodb",region_name="ap-south-1")
        self.table=self.dynamodb.Table(table_name)

    def get_table(self):
        return self.table
