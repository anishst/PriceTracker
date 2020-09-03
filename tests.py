# This is use to run scheduled run in Jenkins
import os
import sys
import time
import uuid
import pytest
sys.path.insert(0, os.getcwd())
from common.database import Database
#
# #  code to check latest price
from app import get_latest_price

Database.initialize()
print("running code...")
items = Database.find('items', {})


@pytest.mark.parametrize("item", items)
def test_check_price_selenium(item):
    try:
        latest_price = get_latest_price(item, headless=False)
        print(f"Checking price for {item['item_desc']}")
        price_item = {
            "_id": uuid.uuid4().hex,
            "script_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "item_url": item["item_url"],
            "price": latest_price,
            "item_id": item["_id"],
        }
        Database.insert('price_history', price_item)
        assert latest_price is not None
    except Exception as e:
        print(f"Something went wrong {e}")
        assert False




