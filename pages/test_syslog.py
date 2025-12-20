from pages.base import base_page
from common.config_read import ConfigRead

class test_syslog(base_page):
    def __init__(self, driver=None):
        super().__init__(driver)
        self.path = [path.strip() for path in self.config.get("syslog_config", "path").splitlines() ]
        self.syslog_config = [config.strip() for config in self.config.get("syslog_config", "config").splitlines()]

    def syslog_config_auto(self):
        # 进入 syslog设置 界面
        for path in self.path:
            path_by_locator = path.split(', ')
            element = self.find_element(*path_by_locator)
            self.click_element(element=element)
        
        import time 
        # 自动操作
        for config in self.syslog_config:
            config_type_by_locator = config.split(', ')
            config_type, config_by_locator = config_type_by_locator[0], \
                config_type_by_locator[1:3]
            element = self.find_element(*config_by_locator)
            if config_type == "click":
                # 如果勾选了，先取消勾选，判断label元素上面同层的input状态
                try:
                    time.sleep(1)
                    input_xpath = config_type_by_locator[2] + '/../input'
                    input_element = self.find_element('xpath', input_xpath)
                    print(input_element.get_attribute("class"))
                    if "not-empty" in input_element.get_attribute("class"):
                        self.click_element(element=element)
                except: pass
                self.click_element(element=element)
            elif config_type == "input":
                # 检测原本输入框中是否有值
                if element.get_attribute('value') != "":
                    element.clear()
                self.input_text(element=element, text=config_type_by_locator[3])

        self.webdriver.save_screenshot(r"backend\screenshot_save\syslog_config.png")        
        # 返回webdriver对象，获取截图作为Base64字符串
        return self.webdriver, self.webdriver.get_screenshot_as_base64()
