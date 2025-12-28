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
            # 第一步：先连接到MySQL服务器但不指定数据库
            connection = mysql.connector.connect(
                host = self.db_config["host"],
                port = self.db_config["port"],
                user = self.db_config["username"],
                password = self.db_config["password"]
            )
            
            if connection.is_connected():
                cursor = connection.cursor()
                
                # 检查数据库是否存在，不存在则创建
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_config['database']}")
                cursor.execute(f"USE {self.db_config['database']}")
                print(f"成功连接到数据库 {self.db_config['database']}")
                
                # 创建users表（如果不存在）
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