import mysql.connector
from mysql.connector import Error
from common.config_read import *

class MysqlConnect():
    def __init__(self,):
        pass

    def get_connection(self):
        try:
            config_read = ConfigRead()
            self.db_config = config_read.config_load()
            connection = mysql.connector.connect(
                host = self.db_config["host"],
                port = self.db_config["port"],
                user = self.db_config["username"],
                password = self.db_config["password"],
                database = self.db_config["database"]
            )

            if connection.is_connected():
                print(f"成功连接到数据库 {self.db_config['database']}")
                return connection

        except Error as e:
            print(f"连接数据库时出错: {e}")
            return None