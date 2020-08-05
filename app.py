import time
import uuid

from flask import Flask, redirect, url_for, request, render_template
from common.database import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)


@app.before_first_request
def init_db():
    Database.initialize()

@app.route("/home", methods=['GET','POST'])
@app.route("/", methods=['GET','POST'])
def home():
    if request.method == 'POST':
        print(request.form)
        new_item = {
            "_id": uuid.uuid4().hex,
            "store_name": request.form['store_name'],
            "item_desc": request.form['item_desc'],
            "item_url": request.form['item_url'],
            "target_price": request.form['target_price']
        }
        Database.insert('items', new_item)
        return redirect(url_for('home'))

    items  =Database.find('items', { })
    prices = Database.find('price_history', { })
    return render_template('home.html', items=items, prices=prices)

@app.route("/check_price_selenium")
def check_price_selenium():
    items = Database.find('items', {})
    for item in items:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)
        try:
            print("Running Chrome Script")

            url = item["item_url"]
            driver.get(url)
            element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='priceblock_dealprice' or @id='priceblock_ourprice']")))
            string_price = element.text.strip()
            print(string_price)
            price_item = {
                "_id":  uuid.uuid4().hex,
                "script_time": time.strftime("%Y-%m-%d %H:%M:%S"),
                "item_url": item["item_url"],
                "price": string_price
            }
            print(items)
            Database.insert('price_history', price_item)
        except Exception as e:
            print(f"Something went wrong while searching.. Details: {e}")
        finally:
            driver.quit()

    return redirect('/home')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
