from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from common.config_read import ConfigRead

class base_page:
    def __init__(self):
        options = Options()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-running-insecure-content')
        # 关键：调试阶段必须注释掉或移除 --headless 参数，才能看到窗口
        # options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--log-level=3')  # 关键：控制浏览器控制台日志级别 (0:INFO, 1:WARNING, 2:ERROR, 3:FATAL)
        options.add_argument('--silent')  # 静默模式，减少输出
        # 可选：隐藏“Chrome正受到自动测试软件控制”的提示栏（不影响窗口显示）
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        self.webdriver = webdriver.Edge(options=options)
        self.webdriver.maximize_window()
        self.webdriver.implicitly_wait(10)

        config = ConfigRead()
        self.config = config.config_load()
        
    def find_element(self, by, locator):
        return self.webdriver.find_element(by, locator)

    def click_element(self, element):
        element.click()

    def input_text(self, element, text):
        element.send_keys(text)

    def wait_for_angular_ready(self):
        """等待AngularJS完成渲染"""
        # 等待AngularJS加载完成
        WebDriverWait(self.webdriver, timeout=5).until(
            lambda d: d.execute_script("return angular.element(document).injector().get('$http').pendingRequests.length === 0;")
        )
    
    def wait_element(self, BY, locator, timeout):
        # 步骤1：等待元素存在
        element = WebDriverWait(self.webdriver, timeout).until(
            EC.presence_of_element_located(BY, locator=locator)
        )
        # 步骤2：等待文本加载
        WebDriverWait(self.webdriver, timeout).until(
            lambda d: element.text.strip() != ""
        )

    def driver_quit(self):
        import time
        time.sleep(5)
        self.webdriver.quit()