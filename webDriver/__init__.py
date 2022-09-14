# -*- encoding=utf-8 -*-
import os
import sys
from base_path import get_base_path
from selenium.webdriver import DesiredCapabilities

if sys.platform.startswith('win'):
    system = 'win'
else:
    system = 'linux'


def set_options(options, proxy):
    if proxy is not None:
        options.add_argument("--proxy-server={0}".format(proxy))
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=800x600')
    options.add_argument('blink-settings=imagesEnabled=false')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--disable-javascript")
    options.add_argument("--headless")
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    return options


def create_driver(browser_type='chrome', proxy=None):
    if browser_type == 'chrome':
        from selenium import webdriver
        options = webdriver.ChromeOptions()
        options = set_options(options, proxy)
        desired_capabilities = DesiredCapabilities.CHROME
        desired_capabilities["pageLoadStrategy"] = 'eager'
        return webdriver.Chrome(
            executable_path=os.path.join(
                get_base_path(), "webDriver", system, 'chromedriver' + ('.exe' if system == 'win' else '')),
            options=options,
            desired_capabilities=desired_capabilities
        )
    elif browser_type == 'edge':
        from msedge.selenium_tools import EdgeOptions, Edge
        options = EdgeOptions()
        options.use_chromium = True
        options = set_options(options, proxy)
        desired_capabilities = DesiredCapabilities.EDGE
        desired_capabilities["pageLoadStrategy"] = 'eager'
        return Edge(
            executable_path=os.path.join(get_base_path(), "webDriver", 'win', 'msedgedriver.exe'),
            options=options,
            desired_capabilities=desired_capabilities
        )
    else:
        raise TypeError('错误的浏览器类型')
