import mysql.connector
from mysql.connector import Error
from common.config_read import *

class MysqlConnect():
    def __init__(self,):
        pass

    def get_connection(self):
        try:
            config_read = ConfigRead()
            self.db_config = config_read.database_load()
            connection = mysql.connector.connect(
                host = self.db_config["host"],
                port = self.db_config["port"],
                user = self.db_config["username"],
                password = self.db_config["password"],
                database = self.db_config["database"]
            )

            if connection.is_connected():
                print(f"成功连接到数据库 {self.db_config['database']}")
                
                # 创建游标
                cursor = connection.cursor()
                
                # 直接尝试创建表（如果不存在）
                create_table_sql = """
                    CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(10) NOT NULL,
                        password VARCHAR(255) NOT NULL,
                        bmc_ip VARCHAR(20),
                        bmc_username VARCHAR(20),
                        bmc_password VARCHAR(255),
                        os_ip VARCHAR(20),
                        os_username VARCHAR(20),
                        os_password VARCHAR(255),
                        file_save_path VARCHAR(100)
                    )
                """
                cursor.execute(create_table_sql)
                connection.commit()
                cursor.close()
                
                return connection

        except Error as e:
            print(f"连接数据库时出错: {e}")
            return None