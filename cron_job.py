# This can used to kick off in Jenkins
import time

from common.database import Database
from common.selenium_mod import get_latest_price
from models.item import Item

Database.initialize()

items = Database.find('items', {})
for item in items:
    latest_price = get_latest_price(item["item_url"])
    price_item = {
        "_id": item["_id"],
        "script_time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "item_url": item["item_url"],
        "price": latest_price
    }
    Database.insert('price_history', price_item)








