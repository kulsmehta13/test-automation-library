import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from retrying import retry

logging.basicConfig(filename='selenium.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SeleniumLib:
    """
    A Selenium-based library to automate browser interactions, such as navigating to URLs, finding elements, 
    waiting for visibility, clicking, and sending input.

    Attributes:
        browser (str): The type of browser to automate (e.g., 'chrome', 'firefox', 'edge').
        driver (WebDriver): The WebDriver instance for controlling the browser.

    Methods:
        connect():
            Starts the WebDriver instance for the specified browser. Retries twice in case of failure.
        close():
            Closes the browser if the WebDriver is active. Retries twice in case of failure.
        navigate_to(url: str):
            Navigates to the specified URL.
        find_element(by: str, value: str):
            Finds a web element using the specified locator method and value.
        wait_for_element_visibility(locator: tuple, timeout: int = 10):
            Waits for an element to be visible on the page for a specified timeout (default is 10 seconds). Retries twice.
        click_element(element: WebElement):
            Clicks on the provided web element. Retries twice.
        send_keys_to_element(element: WebElement, text: str):
            Sends the provided text to the web element.

       Example usage:
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys

        # Initialize SeleniumLib for Chrome
        driver = SeleniumLib(browser='chrome')
        driver.connect()    # Connect to the Chrome browser
        
        driver.navigate_to("https://www.example.com")   # Navigate to a URL
        
        search_box = driver.find_element(By.NAME, "q")  # Find an element by its name attribute

        # Send text to the element
        driver.send_keys_to_element(search_box, "Selenium Python")

        # Wait for a result element to be visible
        result = driver.wait_for_element_visibility((By.ID, "result"))

        # Click on the result element
        driver.click_element(result)

        # Close the browser
        driver.close()
    """
    def __init__(self, browser):
        self.browser = browser
        self.driver = None

    @retry(stop_max_attempt_number=2, wait_fixed=2000)
    def connect(self):
        """
        Initializes and connects the WebDriver for the specified browser.

        The method starts the WebDriver for the browser set during the initialization of the SeleniumLib instance. 
        Supported browsers include Chrome, Firefox, and Edge.

        Raises:
            ValueError: If an unsupported browser is specified.
            Exception: If an error occurs during the WebDriver initialization.

        Example usage:
            # Connect to the Chrome browser
            driver = SeleniumLib(browser='chrome')
            driver.connect()

            # Connect to the Firefox browser
            driver = SeleniumLib(browser='firefox')
            driver.connect()

            # Raises an error for an invalid browser type
            driver = SeleniumLib(browser='invalid_browser')
            driver.connect()  # Raises ValueError
        """
        try:
            logging.info(f"Connecting to {self.browser} browser")
            if self.browser.lower() == "chrome":
                self.driver = webdriver.Chrome()
            elif self.browser.lower() == "firefox":
                self.driver = webdriver.Firefox()
            elif self.browser.lower() == "edge":
                self.driver = webdriver.Edge()
            else:
                raise ValueError("Invalid browser specified")
        except Exception as e:
            logging.error(f"Error occurred during connection: {str(e)}")
            raise

    @retry(stop_max_attempt_number=2, wait_fixed=2000)
    def close(self):
        """
        Closes the active browser session by terminating the WebDriver.

        If the WebDriver is active, this method closes the browser and quits the session. 
        The operation will retry up to 2 times with a 2-second interval if an error occurs.

        Raises:
            Exception: If an error occurs during the browser closing process.

        Example usage:
            # Close the active browser session
            driver.close()
        """
        try:
            logging.info("Closing the browser")
            if self.driver:
                self.driver.quit()
        except Exception as e:
            logging.error(f"Error occurred during browser closing: {str(e)}")
            raise

    def navigate_to(self, url):
        """
        Navigates the browser to the specified URL.

        This method directs the WebDriver to open the given URL in the active browser session.

        Args:
            url (str): The web address to navigate to.

        Raises:
            Exception: If an error occurs during navigation.

        Example usage:
            # Navigate to a specific URL
            driver.navigate_to("https://www.example.com")
        """
        try:
            logging.info(f"Navigating to URL: {url}")
            self.driver.get(url)
        except Exception as e:
            logging.error(f"Error occurred during navigation: {str(e)}")
            raise

    def find_element(self, by, value):
        """
        Finds a web element on the current page using the specified locating strategy.

        Args:
            by (str): The strategy to locate the element (e.g., By.ID, By.NAME, By.XPATH, etc.).
            value (str): The locator value (e.g., the ID, name, or XPath expression to find the element).

        Returns:
            WebElement: The first matching web element found by the specified locating strategy.

        Raises:
            Exception: If the element is not found or an error occurs during the search process.

        Example usage:
            # Find an element by its ID
            element = selenium_lib.find_element(By.ID, "submit-button")

            # Find an element by its name attribute
            element = selenium_lib.find_element(By.NAME, "search-box")
        """
        try:
            logging.debug(f"Finding element by {by}: {value}")
            return self.driver.find_element(by, value)
        except Exception as e:
            logging.error(f"Error occurred while finding element: {str(e)}")
            raise

    def wait_for_element_visibility(self, locator, timeout=10):
        """
        Waits for a web element to become visible on the page within the specified timeout.

        This method uses an explicit wait to pause execution until the element identified by the locator becomes visible.
        The wait will timeout after the specified duration (default is 10 seconds).

        Args:
            locator (tuple): A tuple representing the locating strategy and value (e.g., (By.ID, "element_id")).
            timeout (int, optional): The maximum time to wait for the element's visibility (default is 10 seconds).

        Returns:
            WebElement: The web element if it becomes visible within the timeout period.

        Raises:
            TimeoutException: If the element does not become visible within the specified timeout.
            Exception: For any other errors that occur during the wait process.

        Example usage:
            # Wait for an element to become visible
            element = driver.wait_for_element_visibility((By.ID, "submit-button"), timeout=15)
        """
        try:
            logging.info(f"Waiting for element visibility")
            return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
        except Exception as e:
            logging.error(f"Error occurred while waiting for element visibility: {str(e)}")
            raise

    def click_element(self, element):
        """
        Clicks on the provided web element.

        This method attempts to click the specified web element. If the element is not found or is `None`, an error is raised.

        Args:
            element (WebElement): The web element to be clicked.

        Raises:
            AssertionError: If the element is not found or is `None`.
            Exception: If an error occurs while attempting to click the element.

        Example usage:
            # Find and click a submit button element
            element = driver.find_element(By.ID, "submit-button")
            driver.click_element(element)
        """
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

    def send_keys_to_element(self, element, text):
        """
        Sends the specified text to the provided web element.

        This method inputs the given text into the web element, typically a text field or input area.

        Args:
            element (WebElement): The web element to which the text will be sent.
            text (str): The text to be input into the element.

        Raises:
            Exception: If an error occurs while sending the text to the element.

        Example usage:
            # Find a text field element and send input text
            element = driver.find_element(By.NAME, "username")
            driver.send_keys_to_element(element, "my_username")
        """
        try:
            logging.info(f"Sending keys '{text}' to element")
            element.send_keys(text)
        except Exception as e:
            logging.error(f"Error occurred while sending keys to element: {str(e)}")
            raise
