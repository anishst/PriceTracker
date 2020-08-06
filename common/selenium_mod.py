from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_latest_price(url):
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    try:
        driver.get(url)
        element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='priceblock_dealprice' or @id='priceblock_ourprice']")))
        string_price = element.text.strip()
        print(string_price)
        price = string_price
    except Exception as e:
        print(f"Something went wrong while searching.. Details: {e}")
    finally:
        driver.quit()
    return price