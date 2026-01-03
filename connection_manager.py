import boto
import boto.dynamodb2
from boto.dynamodb2.table import Table
from boto.dynamodb2.fields import HashKey
import ConfigParser
from boto.exception import JSONResponseError


class ConnectionManager:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        self.table_name = self.config.get("Settings", "TableName")
        self.region = self.config.get("dynamodb", "region")
        self.connect()

    def load_config(self, config_path):
        config = ConfigParser.ConfigParser()
        config.read(config_path)
        return config

    def connect(self):
        self.conn = boto.dynamodb2.connect_to_region(self.region)

    def table_exists(self):
        try:
            self.conn.describe_table(self.table_name)
            return True
        except JSONResponseError as e:
            if e.error_code == "ResourceNotFoundException":
                return False
            raise

    def create_table(self):
        Table.create(
            self.table_name,
            schema=[HashKey("GameId")],
            throughput={"read": 5, "write": 5},
            connection=self.conn
        )
        print("DynamoDB table created:", self.table_name)

    def get_table(self):
        if not self.table_exists():
            self.create_table()
        else:
            print("DynamoDB table already exists:", self.table_name)

        return Table(self.table_name, connection=self.conn)
