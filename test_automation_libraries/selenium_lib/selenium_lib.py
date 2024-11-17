import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from retrying import retry

logging.basicConfig(filename='selenium.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
print("Hello world!!")
class SeleniumLib:
    def __init__(self, browser):
        self.browser = browser
        self.driver = None

    @retry(stop_max_attempt_number=2, wait_fixed=2000)
    def connect(self):
        try:
            logging.info(f"Connecting to {self.browser} browser")
            if self.browser == "chrome":
                self.driver = webdriver.Chrome()
            elif self.browser == "firefox":
                self.driver = webdriver.Firefox()
            elif self.browser == "edge":
                self.driver = webdriver.Edge()
            else:
                raise ValueError("Invalid browser specified")
        except Exception as e:
            logging.error(f"Error occurred during connection: {str(e)}")
            raise

    @retry(stop_max_attempt_number=2, wait_fixed=2000)
    def close(self):
        try:
            logging.info("Closing the browser")
            if self.driver:
                self.driver.quit()
        except Exception as e:
            logging.error(f"Error occurred during browser closing: {str(e)}")
            raise

    @retry(stop_max_attempt_number=2, wait_fixed=2000)
    def navigate_to(self, url):
        try:
            logging.info(f"Navigating to URL: {url}")
            self.driver.get(url)
        except Exception as e:
            logging.error(f"Error occurred during navigation: {str(e)}")
            raise

    @retry(stop_max_attempt_number=2, wait_fixed=2000)
    def find_element(self, by, value):
        try:
            logging.debug(f"Finding element by {by}: {value}")
            return self.driver.find_element(by, value)
        except Exception as e:
            logging.error(f"Error occurred while finding element: {str(e)}")
            raise

    @retry(stop_max_attempt_number=2, wait_fixed=2000)
    def wait_for_element_visibility(self, locator, timeout=10):
        try:
            logging.info(f"Waiting for element visibility")
            return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
        except Exception as e:
            logging.error(f"Error occurred while waiting for element visibility: {str(e)}")
            raise

    @retry(stop_max_attempt_number=2, wait_fixed=2000)
    def click_element(self, element):
        try:
            logging.info("Clicking on element")
            if element:
                element.click()
            else:
                logging.error("Element not found")
                raise AssertionError("Element not found")
        except Exception as e:
            logging.error(f"Error occurred while clicking on element: {str(e)}")
            raise

    @retry(stop_max_attempt_number=2, wait_fixed=2000)
    def send_keys_to_element(self, element, text):
        try:
            logging.info(f"Sending keys '{text}' to element")
            element.send_keys(text)
        except Exception as e:
            logging.error(f"Error occurred while sending keys to element: {str(e)}")
            raise
