# This is use to run scheduled run in Jenkins
from common.database import Database
import  app

#  code to check latest price
Database.initialize()
# app.check_price_selenium()

items = Database.find('items', {})
# print([item for item in items])
itemsList = [item for item in items]
new_list = []

new_dict = {}
for item in itemsList:
    print(type(item))
    # get latest price
    myquery = {"item_id": item["_id"]}
    mydoc = Database.find('price_history', myquery).sort("script_time", -1).limit(1)
    print(item["item_desc"],item["target_price"])
    new_dict["item_desc"] = item["item_desc"]
    new_dict["target_price"] = item["target_price"]
    print("Latest price...")
    myquery = { "item_id": item["_id"]}
    mydoc = Database.find('price_history',myquery).sort("script_time", -1).limit(1)
    for x in mydoc:
        print(x["script_time"],x['price'])
        new_dict['latest_price_check'] = x["script_time"]
        new_dict['latest_price'] = x["price"]

    print("Chepest price...")
    myquery = { "item_id": item["_id"]}
    mydoc = Database.find('price_history',myquery).sort("price", 1).limit(1)
    for x in mydoc:
        print(x["script_time"],x['price'])
        new_dict['chepest_price_check'] = x["script_time"]
        new_dict['chepest_price'] = x["price"]
    print("*"*100)
    new_list.append(new_dict)

print(new_list)
# x   = []
# cur = Database.find('items', {})
# for i in cur:
#     x.append(i)
# print(x)



