import time
import uuid
from flask import Flask, redirect, url_for, request, render_template, flash
from common.database import *
from common.util import get_latest_price


app = Flask(__name__)
app.secret_key = "abcdef133"


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
    #TODO : FIND A WAY TO SHOW LATEST PRICE on home page
    latest_item = Database.find('price_history', {}).sort("script_time", -1).limit(1)
    # items  =Database.find('items', { })
    items = Database.find('items', {})
    # print([item for item in items])
    itemsList = [item for item in items]
    new_list = []


    for item in itemsList:
        new_dict = {} # temp dict
        # get item

        #  copy all items to temp dict
        new_dict = item.copy()
        print(new_dict)
        print("Latest price...")
        myquery = {"item_id": item["_id"]}
        mydoc = Database.find('price_history', myquery).sort("script_time", -1).limit(1)
        for x in mydoc:
            print(x["script_time"], x['price'])
            new_dict['latest_price_check'] = x["script_time"]
            new_dict['latest_price'] = x["price"]

        print("Cheapest price...")
        # skip None values
        myquery = {"item_id": item["_id"],
                   "price": {"$ne": None}}
        mydoc = Database.find('price_history', myquery).sort("price", 1).limit(1)
        for n in mydoc:
            print(n["script_time"], n['price'])
            new_dict['cheapest_price_check'] = n["script_time"]
            new_dict['cheapest_price'] = n["price"]
        print("*" * 100)
        new_list.append(new_dict)

    return render_template('home.html', items=new_list, latest_item=latest_item)

@app.route("/details/<string:item_id>", methods=['GET','POST'])
def details(item_id):
    if request.method == 'POST':
        print(request.form)
        pass
    print(item_id)
    items  =Database.find('items',{'_id': item_id})
    # price hisotry sorted in desc order latest price on top
    prices = Database.find('price_history', { 'item_id': item_id}).sort("script_time", -1)
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
        if latest_price:
            price_item = {
                "_id": uuid.uuid4().hex,
                "script_time": time.strftime("%Y-%m-%d %H:%M:%S"),
                "item_url": item["item_url"],
                "price": latest_price,
                "item_id": item["_id"],
            }
            Database.insert('price_history', price_item)

    return redirect('/home')

@app.route("/deal_sites")
def deal_sites():
    return render_template("deal_sites.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
