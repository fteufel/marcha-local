from airtable import airtable #https://github.com/josephbestjames/airtable.py
from woocommerce import API #https://github.com/woocommerce/wc-api-python

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

# print(wcapi.get("products/997").json()['date_modified_gmt'])
# print("\n")
# # vends = wcapi.get("\a").json()
# # print(vends)
# products = list()
# product_page = 0
# while True:
#     product_page = product_page + 1
#     query = "products?page={}".format(product_page)
#     prods_page = wcapi.get(query).json()
#     products.append(prods_page)
#     if len(prods_page) < 10:
#         break

# vendors = {}
# categories = {}
# cats = wcapi.get("products/categories").json()

# for cat in cats:
#     cat_id = cat['id']
#     cat_name = cat['name']
#     if not categories.get(cat_name):
#         categories[cat_name] = cat_id

# print(categories)
# for product_page in products:
#     for product in product_page:
#         store_id = product["vendor"]
#         store_name = product["store_name"]
#         if not vendors.get(store_name):
#                 vendors[store_name] = store_id

# print(wcapi.get("orders").json())   


