from airtable import airtable #https://github.com/josephbestjames/airtable.py
from woocommerce import API #https://github.com/woocommerce/wc-api-python
from datetime import datetime, timezone
import dateutil.parser

### APIs
API_KEY = 'keyO4pjsHsgtCPofA'
BASE_ID = 'app1fFJJYvoUtSQUL'
TABLE_NAME = 'Inventory'

wcapi = API(
    url="https://marchalocal.ch",
    consumer_key= 'ck_7e032301f2b9c73f376bf3f608b7274ca27ce020',
    consumer_secret="cs_6ffda704beefd69e0f771b8bfb01297a53101bf8",
    wp_api=True,
    version="wc/v3",
    timeout=15
)

at = airtable.Airtable(BASE_ID, API_KEY)
table = at.get(TABLE_NAME, filter_by_formula= None)

## create record_id dictionary
rec_ids = {}
for record in table["records"]:
    product = record['fields']['Product']
    rec_id = record['id']
    if not rec_ids.get(product):
        rec_ids[product] = rec_id

## Fetch orders from WooCommerce
order_pages = list()
order_page = 0
while True:
    order_page = order_page + 1
    query = "orders?page={}".format(order_page)
    ords_page = wcapi.get(query).json()
    order_pages.append(ords_page)
    if len(ords_page) < 10:
        break

## Make orders dictionary
orders = {}
for order_page in order_pages:
    for order in order_page:
        order_id = order["id"]
        timestamp = order['date_created_gmt']
        order_date = dateutil.parser.parse(timestamp +"+00:00")
        items = list()
        for item in order['line_items']:
            prod_id = item['product_id']
            prod_name = item["name"]
            qty = item['quantity']
            it = {"id": prod_id, "name": prod_name, "quantity": qty, "date": order_date}
            items.append(it)
        if not orders.get(order_id):
            orders[order_id] = {"id": order_id, "items": items}


## Update values in airtable
for order in orders:
    for item in orders[order]["items"]:
        item_bought = item['name']
        number_bought = item['quantity']
        # try:
        #     at_time = at.get("Inventory", record_id=rec_ids[item_bought], fields="Last modified time")
        #     at_stock = at.get("Inventory", record_id=rec_ids[item_bought], fields="Stock")
            
        #     print(at_stock)
        #     last_update_time = dateutil.parser.parse(at_time)

        #     if item["date"] > last_update_time:
        #         new_stock = at_stock - number_bought
        #         resp = at.update("Inventory", rec_ids[item_bought], {"Stock": new_stock })
        # except:
        #     print("Item {} not found in airtables".format(item_bought))
        if rec_ids.get(item_bought):
            at_time = at.get("Inventory", record_id=rec_ids[item_bought])["fields"]["Last modified time"]
            at_stock = at.get("Inventory", record_id=rec_ids[item_bought])["fields"]["Stock"]
            
            last_update_time = dateutil.parser.parse(at_time)

            if item["date"] > last_update_time:
                new_stock = at_stock - number_bought
                resp = at.update("Inventory", rec_ids[item_bought], {"Stock": new_stock })
                print("Restocked {} to {}".format(item_bought, new_stock))