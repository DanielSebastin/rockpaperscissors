import boto
import boto.dynamodb2
from boto.dynamodb2.table import Table
from boto.dynamodb2.fields import HashKey
from boto.dynamodb2.exceptions import ResourceInUseException
import ConfigParser


class ConnectionManager:
    def __init__(self,config_path):
        self.config=self.load_config(config_path)
        self.table_name=self.config.get("Settings","TableName")
        self.region=self.config.get("dynamodb","region")

    def load_config(self,config_path):
        config=ConfigParser.ConfigParser()
        config.read(config_path)
        return config

    def connect(self):
        boto.dynamodb2.connect_to_region(self.region)

    def create_table_if_not_exists(self):
        try:
            Table.create(
                self.table_name,
                schema=[HashKey("GameId")],
                throughput={"read":5,"write":5}
            )
            print("DynamoDB table created:",self.table_name)
        except ResourceInUseException:
            print("DynamoDB table already exists:",self.table_name)

    def get_table(self):
        self.connect()
        self.create_table_if_not_exists()
        return Table(self.table_name)
