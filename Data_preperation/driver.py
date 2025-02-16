import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

#------------------------------------------------------------------------------------------------------------------

def initialize_driver():
    """Initializes and returns a Selenium driver in headless mode."""
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Silent mode
    return webdriver.Chrome(service=service, options=options)

#------------------------------------------------------------------------------------------------------------------

def scroll_page(driver, scroll_attempts=3):
    """Scrolls down the page to load more tweets."""
    prev_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(scroll_attempts):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == prev_height:
            break
        prev_height = new_height

#------------------------------------------------------------------------------------------------------------------

def click_load_more(driver):
    """Clicks only on the 'Load more' button and ignores 'Load newest'."""
    try:
        load_more_buttons = driver.find_elements(By.CSS_SELECTOR, "div.show-more a")
        for button in load_more_buttons:
            if "Load more" in button.text:  # Checks if it's indeed 'Load more'
                button.click()
                time.sleep(2)  # Wait for new tweets to load
                return True
        return False  # No 'Load more' button found
    except Exception as e:
        print(f"Error clicking 'Load more': {e}")
        return False
