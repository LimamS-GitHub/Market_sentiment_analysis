import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth

#------------------------------------------------------------------------------------------------------------------

CHROMEDRIVER_PATH = ChromeDriverManager().install()

def initialize_driver(selected_proxy):
    print(f"Utilisation du proxy : {selected_proxy}")

    # Config Chrome
    options = webdriver.ChromeOptions()
    options.add_argument(f'--proxy-server=http://{selected_proxy}')
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
    )
    service = Service(CHROMEDRIVER_PATH)
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
            if "Load more" in button.text:
                button.click()
                time.sleep(2)
                return True
        return False
    except Exception as e:
        print(f"Error clicking 'Load more': {e}")
        return False
