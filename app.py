from flask import Flask, redirect, url_for, request, render_template
from database import *

app = Flask(__name__)


@app.before_first_request
def init_db():
    Database.initialize()

@app.route("/home", methods=['GET','POST'])
@app.route("/", methods=['GET','POST'])
def home():
    if request.method == 'POST':
        new_item = {
            "store_name": request.form['store_name'],
            "item_url": request.form['item_url'],
            "target_price": request.form['target_price']
        }

        Database.insert('items', new_item)
        return redirect(url_for('home'))

    items  =Database.find('items', {})
    return render_template('home.html', items=items)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
