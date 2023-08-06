import os
import platform
from typing import Any
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement

from material_zui.selenium.common import safe_find_element
from material_zui.fake import random_sleep
from material_zui.list import map_to


class Zui_Selenium_Chrome:
    def __init__(self) -> None:
        self.is_mac = False
        if not any(os_name in platform.platform() for os_name in ["Windows", "Linux"]):
            self.is_mac = True

    @property
    def screen_height(self) -> int:
        return self.driver.execute_script("return window.screen.height;")

    @property
    def scroll_height(self) -> int:
        return self.driver.execute_script("return document.body.scrollHeight;")

    @property
    def page_source(self) -> str: return self.driver.page_source

    @property
    def document(self) -> BeautifulSoup:
        return BeautifulSoup(self.driver.page_source, "html.parser")

    def connect(self):
        self.driver = webdriver.Chrome()
        return self.driver

    def connect_debug(self, port: int = 9000, debug_address: str = ''):
        '''
        @port: port number, default `9000`
        @debug_address: format `127.0.0.1:9000`, default `localhost:{port}`
        - Use for case need authorization, you just need to start `chrome beta` -> login account -> close browswer then
            - start `chrome` on debug mode -> call this method to connect to browser opened
        1. Install `chrome beta` for better automation: https://www.google.com/chrome/beta
        2. Start `chrome` by command: `google-chrome-beta --remote-debugging-port={port}`
                - `port` must the same with input parameter of this method
        '''
        debug_address = debug_address or f"localhost:{port}"
        self.options = Options()
        self.options.add_experimental_option(
            "debuggerAddress", debug_address)
        self.driver = webdriver.Chrome(options=self.options)
        return self.driver

    def delay(self, sec: float = 0) -> None:
        random_sleep(1, 5, sec)

    def safe_find_element(
            self, by: str = By.ID,
            value: str | None = None,
            parent: Any = None) -> WebElement | None:
        '''
        This is safe find element method
        @return `None` in case not found
        '''
        return safe_find_element(parent if parent else self.driver, by, value)

    def safe_find_element_by_xpath(self, xpath_value: str) -> WebElement | None:
        return self.safe_find_element(By.XPATH, xpath_value)

    def find_element_by_xpath(self, xpath_value: str): return self.driver.find_element(
        By.XPATH, xpath_value)

    def find_elements_by_xpath(self, xpath_value: str): return self.driver.find_elements(
        By.XPATH, xpath_value)

    def find_elements_by_class(self, class_value: str): return self.driver.find_elements(
        By.CLASS_NAME, class_value)

    def scroll_to_end(self) -> None:
        self.driver.execute_script("window.scrollTo(0, {scroll_height});".format(
            scroll_height=self.scroll_height))

    def scroll(self, step_scroll: int) -> None:
        for index in range(step_scroll):
            print(index+1, "Scrolling to", self.scroll_height)
            self.scroll_to_end()
            self.delay()

    def get_urls(self, class_selector: str) -> list[str]:
        '''
        Get video urls by class selector of each video
        '''
        videos = self.document.find_all(
            "div", {"class": class_selector})
        return map_to(videos, lambda video, _: video.a["href"])

    def switch_to_frame(self, xpath_value: str) -> None:
        '''
        @xpath_value: must be end with `frame/iframe` like `//*[@id="main"]/div[2]/div/iframe`
        '''
        frame_element = self.find_element_by_xpath(xpath_value)
        self.driver.switch_to.frame(frame_element)

    def upload_file(self, xpath_value: str, video_relative_path: str) -> None:
        '''
        @xpath_value: must be end with `input` like `//*[@id="root"]/div/div/div/div/div/div/div/input`
        @video_relative_path: video relative path, from root project directory
        '''
        file_input = self.find_element_by_xpath(xpath_value)
        abs_path = os.path.abspath(video_relative_path)
        file_input.send_keys(abs_path)

    def click(self, xpath_value: str):
        '''
        Click then return that element
        '''
        element = self.find_element_by_xpath(xpath_value)
        element.click()
        return element

    def safe_click(self, xpath_value: str):
        '''
        Safe click element
        '''
        try:
            element = self.safe_find_element_by_xpath(xpath_value)
            if element:
                element.click()
            return element
        except:
            return None

    def send_keys(self, xpath_value: str, key_value: str, clear_before_send_keys: bool = True, delay_time: int = 10):
        '''
        Send keys then return that element
        @xpath_value: only valid with element selector can input value
        @clear_before_send_keys:
        - True: clear input before send keys
        - False: value will input after existed value
        '''
        # element = self.find_element_by_xpath(xpath_value)
        element = self.wait_get(xpath_value, delay_time)
        element.click()
        if clear_before_send_keys:
            element.send_keys(Keys.CONTROL + 'a')
            element.send_keys(Keys.BACKSPACE)
        element.send_keys(key_value)
        return element

    # def wait_get(self, xpath_value: str, delay_time: int = 10) -> WebElement:
    #     element: Any = WebDriverWait(self.driver, delay_time).until(  # using explicit wait for 10 seconds
    #         EC.presence_of_element_located(
    #             (By.XPATH, xpath_value))  # finding the element
    #     )
    #     return element
    def wait_get(self, xpath_value: str, delay_time: int = 10, time_to_try: int = 10) -> WebElement:
        for _ in range(time_to_try):
            element = self.safe_find_element_by_xpath(xpath_value)
            if element:
                return element
            self.delay(delay_time)
        return WebDriverWait(self.driver, delay_time).until(  # using explicit wait for 10 seconds
            EC.presence_of_element_located(
                (By.XPATH, xpath_value))  # finding the element
        )
