from pages.base import base_page
from common.config_read import ConfigRead

class test_snmp_trap(base_page):
    def __init__(self, driver=None):
        super().__init__(driver)
        self.meau_expand = self.config.get("snmp_trap_config", "meau_expand").split(', ')
        self.path = [path.strip() for path in self.config.get("snmp_trap_config", "path").splitlines() ]
        self.snmp_trap_config = [config.strip() for config in self.config.get("snmp_trap_config", "config").splitlines()]

    def snmp_trap_config_auto(self):
        # 判断 BMC设置 菜单是否展开
        meau_element = self.find_element(*self.meau_expand)
        _path = self.path[1:] if "menu-show" in meau_element.get_attribute("class") else self.path
        # 依次点击进入 snmp trap设置 界面
        for path in _path:
            path_by_locator = path.split(', ')
            element = self.find_element(*path_by_locator)
            self.click_element(element=element)
        
        import time 
        # 自动操作
        for config in self.snmp_trap_config:
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

        self.webdriver.save_screenshot(r"backend\screenshot_save\snmp_trap_config.png")        
        # 返回webdriver对象，获取截图作为Base64字符串
        return self.webdriver, self.webdriver.get_screenshot_as_base64()
