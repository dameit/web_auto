from pages.base import base_page
from common.config_read import ConfigRead

class test_syslog(base_page):
    def __init__(self):
        super().__init__()
        self.path = [path.strip() for path in self.config.get("syslog_config", "path").splitlines() ]
        self.syslog_config = [config.strip() for config in self.config.get("syslog_config", "config").splitlines()]

    def syslog_config_auto(self):
        # 进入 syslog设置 界面
        for path in self.path:
            path_by_locator = path.split(', ')
            element = self.find_element(*path_by_locator)
            self.click_element(element=element)
        
        # 自动操作
        for config in self.syslog_config:
            config_type_by_locator = config.split(', ')
            config_type, config_by_locator = config_type_by_locator[0], \
                config_type_by_locator[1:3]
            element = self.find_element(*config_by_locator)
            if config_type == "click":
                self.click_element(element=element)
            elif config_type == "input":
                self.input_text(element=element, text=config_type_by_locator[3])
