import time
import uuid

from flask import Flask, redirect, url_for, request, render_template, flash
from common.database import *
from common.util import get_latest_price
from models.item import Item
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from models.item import Item

app = Flask(__name__)
app.secret_key = "123"


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
    return render_template('home.html', items=items)

@app.route("/details/<string:item_id>", methods=['GET','POST'])
def details(item_id):
    if request.method == 'POST':
        print(request.form)
        pass
    print(item_id)
    items  =Database.find('items',{'_id': item_id})
    prices = Database.find('price_history', { 'item_id': item_id})
    return render_template('details.html', items=items, prices=prices)

@app.route("/edit_item/<string:item_id>", methods=['GET','POST'])
def edit_item(item_id):
    if request.method == 'POST':
        updated_item = {
            # "_id": item_id,
            "store_name": request.form['store_name'],
            "item_desc": request.form['item_desc'],
            "item_url": request.form['item_url'],
            "target_price": request.form['target_price']
        }
        Database.update('items',{'_id': item_id},updated_item)
        flash(f"Updated {item_id}", 'success')
        return redirect(url_for('home'))

    item  =Database.find_one('items',{'_id': item_id})

    return render_template('edit_item.html', item=item)

@app.route("/delete_item/<string:item_id>")
def delete_item(item_id):
    print(item_id)
    #  remove item
    items  =Database.find_one('items',{'_id': item_id})
    Database.remove('items', items)
    # remove history for items
    delete_history = Database.remove('price_history',{'item_id': item_id})
    flash(f"Removed {items}",'success')
    return redirect(url_for('home'))

#  test version
@app.route("/check_price_selenium")
def check_price_selenium():
    items = Database.find('items', {})
    for item in items:
        latest_price = get_latest_price(item)
        price_item = {
            "_id": uuid.uuid4().hex,
            "script_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "item_url": item["item_url"],
            "price": latest_price,
            "item_id": item["_id"],
        }
        Database.insert('price_history', price_item)

    return redirect('/home')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
