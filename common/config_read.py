import configparser
import os

class ConfigRead():
    def __init__(self, config_file="config.ini"):
        self.config_file = config_file

    def config_load(self):
        try:
            if not os.path.exists(self.config_file):
                # 尝试在项目根目录查找
                base_dir = Path(__file__).resolve().parent.parent
                config_path = base_dir / self.config_file
                if not config_path.exists():
                    raise FileNotFoundError(f"配置文件 {self.config_file} 不存在")
                self.config_file = str(config_path)
            
            # 创建配置解析器
            self.config = configparser.ConfigParser()
            
            # 读取配置文件
            self.config.read(self.config_file, encoding='utf-8')
            
            return self.config
            
        except FileNotFoundError as e:
            print(f"错误: {e}")
            return False
        except KeyError as e:
            print(f"配置错误: {e}")
            return False
        except Exception as e:
            print(f"加载配置文件时出错: {e}")
            return False

    def database_load(self):
        config = self.config_load()

        # 检查是否有database部分
        if config is False or not config.has_section('database'):
            raise KeyError("配置文件中缺少 [database] 部分")
        
        # 提取数据库配置
        db_config = {
            'host': config.get('database', 'host'),
            'port': config.getint('database', 'port', fallback=3306),
            'username': config.get('database', 'username'),
            'password': config.get('database', 'password'),
            'database': config.get('database', 'database'),
        }
        
        # print("数据库配置加载成功")
        return db_config

    def redfish_load(self):
        config = self.config_load()

        redfish_path = {
            'session_post_api': config.get('redfish_path', 'session_post_api')
        }

        return redfish_path
    
    def file_save_path(self):
        config = self.config_load()
        return config.get('file_save_path', 'save_path')