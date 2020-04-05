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

for record in table["records"]:
    ## Not functional yet... : (
    try:
        stock = record["fields"]["Stock"]
        wc_id = record["fields"]["woocommerce_ID"]
        data = {
        "stock_quantity": stock
    }
        wcapi.put("products/{}".format(wc_id), data).json()
    except:
        print("Item {} not in online store...".format(record["fields"]["Product"]))
