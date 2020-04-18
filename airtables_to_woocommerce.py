'''
fteufel
load records from airtable, reformat and push as product into woocommerce
'''

#################################SETUP############################################################################################
### Imports
from airtable import airtable #https://github.com/josephbestjames/airtable.py
from IPython import embed
from woocommerce import API #https://github.com/woocommerce/wc-api-python
from datetime import datetime, timezone
import posixpath
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





#########################################MORE SETUP##############################################################################
### Function declarations

#### database: the whole thing i.e. at 
#### record (from database["records"])
#### metadata: info of categories and vendors (ids and names), dictionary
def airtable_record_to_json(database, record, metadata):
    product = record['fields']['Product']
    price   = record['fields']['Price']
    stock   = record['fields']['Stock']
    description = record['fields']['Description']
    img_url = record["fields"]["Image"][0]['url'] ##['Image is an OrderedDict inside a List, for some reason]
    category = record['fields']["ProductCategory"]
    
    #relational lookups
    merchant_record = record['fields']['Store'][0] #array again

    vendor_info = database.get('Vendors', record_id=merchant_record, limit=0, offset=None, filter_by_formula=None, view=None, max_records=0, fields=[])['fields']
    store = vendor_info['Store']
    group_id =  vendor_info['Groups'][0] # is still in array, could also loop for multiple group assignments
    group_info = database.get('Location', record_id=group_id, limit=0, offset=None, filter_by_formula=None, view=None, max_records=0, fields=[])['fields']
    group_name = group_info['Location']
    vendor_id = metadata['vendors'][store]
    
    if not metadata['categories'].get(category):
        data = {
            "name": category
        }
        resp = wcapi.post("products/categories", data).json()
        metadata['categories'][category] = resp['id']
    category_id = metadata['categories'][category]
    
    #reformat
    data = {
        "name": product,
        "type": "simple", 
        "regular_price": str(price),
        "description": description,
        "short_description": description,
        "vendor": vendor_id,
        "categories": [
            {
                'id': category_id
            }
        ],
        "attributes": [
            {
                'id': 1, 
                'name': "Store" ,
                'position': 0, 
                'visible': True, 
                'variation': False, 
                'options': [store]
                },
            {
                'id': 2, 
                'name': 'Store Group', 
                'position': 1, 
                'visible': True, 
                'variation': False, 
                'options': [group_name]
                }
        ],
        "images": [
            {
                'src': img_url,
                "name": product.join(" image")
            }
        ]
    }
    return data

############################################################################################################################
## This Felix is working on, I still don't know what he planned
###### See the data stored for one product in WooCommerce format
# print(wcapi.get("products").json()[0])



#delete all IDs that need to be updated
# Force delete example.
# wcapi.post("products", data)
# print(wcapi.delete("products/100", params={"force": True}).json())

#################################################################ACTUAL CODE DOING STUFF##################################
#super naive implementation, iterate over all records and update



### get vendors from existing products (only if already declared, can't get them from wcmp yet)
products = list()
product_page = 0
while True:
    product_page = product_page + 1
    query = "products?page={}".format(product_page)
    prods_page = wcapi.get(query).json()
    products.append(prods_page)
    if len(prods_page) < 10:
        break

vendors = {}
categories = {}
### Note, all categories mentioned in the airtable need to be created manually in the wordpress
cats = wcapi.get("products/categories").json()

for cat in cats:
    cat_id = cat['id']
    cat_name = cat['name']
    if not categories.get(cat_name):
        categories[cat_name] = cat_id

for product_page in products:
    for product in product_page:
        store_id = product["vendor"]
        store_name = product["store_name"]
        if not vendors.get(store_name):
                vendors[store_name] = store_id

metadata = {"vendors": vendors, "categories": categories}
### Table import
at = airtable.Airtable(BASE_ID, API_KEY)
table = at.get(TABLE_NAME, filter_by_formula= None)

### Record: dict for each entry in Table
for idx, record in enumerate(table['records']):
    print("Parsing entry {} of {}".format(idx+1, len(table["records"])))
    #filter by time, don't update everything
    ### Seems to be not completely perfect yet
    at_time = record['fields']['Last modified time']
    last_update_time = dateutil.parser.parse(at_time)
    try:
        woocommerce_ID = record['fields']['woocommerce_ID']
        wp_time = wcapi.get("products/{}".format(woocommerce_ID)).json()['date_modified_gmt']
        timestamp = dateutil.parser.parse(wp_time +"+00:00")
    except:
        timestamp = datetime.now(timezone.utc)

    if timestamp < last_update_time:
        #delete the old version of the product

        wcapi.delete("products/{}".format(woocommerce_ID), params={"force": True}).json()

        product = airtable_record_to_json(at, record, metadata)
        response = wcapi.post("products", product).json()

    #def update(self, table_name, record_id, data):
    #    if check_string(table_name) and check_string(record_id):
    #        url = posixpath.join(table_name, record_id)
    #        payload = create_payload(data)
    #        return self.__request('PATCH', url,
    #
    # self.headers.update({'Content-type': 'application/json'})
    #    r = requests.request(method,
    #                         posixpath.join(self.base_url, url),
    #                         params=params,
    #                         data=payload,
    #                         headers=self.headers)
    #    if r.status_code == requests.codes.ok:
    #        return r.json(object_pairs_hook=self._dict_class)                              payload=json.dumps(payload))


        #update ID in airtable
        fields = {'woocommerce_ID': str(response['id'])}
        resp = at.update_custom(TABLE_NAME,record['id'], fields)
print("done : ) :) :  )")

# response = wcapi.post("products", product).json()
# response['id']