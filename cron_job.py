# This can used to kick off in Jenkins
import time
import uuid

from common.database import Database
from common.util import get_latest_price

Database.initialize()

items = Database.find('items', {})
for item in items:
    latest_price = get_latest_price(item)
    price_item = {
        "_id": uuid.uuid4().hex,
        "script_time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "item_url": item["item_url"],
        "price": latest_price
    }
    Database.insert('price_history', price_item)








