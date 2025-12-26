from pages.base import base_page
from pages.login import login_page
from common.config_read import ConfigRead
import time

class test_log(base_page):
    def __init__(self, driver, is_before):
        super().__init__(driver)
        self.meau_expand = self.config.get("log_config", "meau_expand").split(', ')
        self.path = [path.strip() for path in self.config.get("log_config", "path").splitlines() ]
        self.log_config = [config.strip() for config in self.config.get("log_config", "config").splitlines()]
        self.is_before = is_before

    def log_config_auto(self):
        # 判断 日志 菜单是否展开
        self.wait_for_angular_ready()
        meau_element = self.find_element(*self.meau_expand)
        _path = self.path[1:] if "menu-show" in meau_element.get_attribute("class") else self.path
        if self.is_before == True:
            # 依次点击进入 日志设置 界面
            for path in _path:
                path_by_locator = path.split(', ')
                if path_by_locator[0] != "click_save_too":
                    path_by_locator = path_by_locator[1:]
                    element = self.find_element(*path_by_locator)
                    self.click_element(element=element)
            
            screenshot_all = []
            # 自动操作
            for config in self.log_config:
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
                    time.sleep(1)
                    if element.get_attribute('value') != "":
                        element.clear()
                    self.input_text(element=element, text=config_type_by_locator[3])
                elif config_type == "select_choose":
                    from selenium.webdriver.support.ui import Select
                    permission_select = Select(element)
                    permission_select.select_by_visible_text(config_type_by_locator[-1])
                elif config_type == "click_save":
                    self.click_element(element=element)
                    screenshot_all.append(self.webdriver.get_screenshot_as_base64())   
        
            # 返回webdriver对象，获取截图作为Base64字符串
            return self.webdriver, screenshot_all

        else:
            screenshot_all = []
            for path in _path:
                path_by_locator = path.split(', ')
                config_type, config_by_locator = path_by_locator[0], path_by_locator[1:]
                element = self.find_element(*config_by_locator)
                self.click_element(element=element)
                time.sleep(1)
                if config_type != "click":
                    screenshot_all.append(self.webdriver.get_screenshot_as_base64())   
            return self.webdriver, screenshot_all