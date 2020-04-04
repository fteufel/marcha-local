'''
fteufel
load records from airtable, reformat and push as product into woocommerce
'''

#################################SETUP############################################################################################
### Imports
from airtable import airtable #https://github.com/josephbestjames/airtable.py
from IPython import embed
from woocommerce import API #https://github.com/woocommerce/wc-api-python

### APIs
API_KEY = 'keyO4pjsHsgtCPofA'
BASE_ID = 'app1fFJJYvoUtSQUL'
TABLE_NAME = 'Inventory'

wcapi = API(
    url="http://marchalocal.ch",
    consumer_key= 'ck_8239347f0b5b3cf8099e3eff1dc0ef398f23cfa8',
    consumer_secret="cs_3360619c363b5d00a254d6b9636b11a0b5a8c63b",
    wp_api=True,
    version="wc/v3",
    timeout=15
)

### Table import
at = airtable.Airtable(BASE_ID, API_KEY)
table = at.get(TABLE_NAME)
#table = at.get(TABLE_NAME)
#vendors_table = at.get('Vendors')

#########################################MORE SETUP##############################################################################
### Function declarations

#### database: the whole thing i.e. at 
#### index: record (from database["records"])
def airtable_record_to_json(database, record):
    product = record['fields']['Product']
    price   = record['fields']['Price']
    stock   = record['fields']['Stock']
    description = record['fields']['Description']
    img_url = record["fields"]["Image"][0]['url'] ##['Image is an OrderedDict inside a List, for some reason]

    #relational lookups
    merchant_record = record['fields']['Store'][0] #array again

    vendor_info = database.get('Vendors', record_id=merchant_record, limit=0, offset=None, filter_by_formula=None, view=None, max_records=0, fields=[])['fields']
    store = vendor_info['Store']
    group_id =  vendor_info['Groups'][0] # is still in array, could also loop for multiple group assignments
    group_info = database.get('Location', record_id=group_id, limit=0, offset=None, filter_by_formula=None, view=None, max_records=0, fields=[])['fields']
    group_name = group_info['Name']
    
    #reformat
    data = {
        "name": product,
        "type": "simple",
        "regular_price": str(price),
        "description": description,
        "short_description": description,
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

### Record: dict for each entry in Table
for idx, record in enumerate(table['records']):
    print("Parsing entry {} of {}".format(idx+1, len(table["records"])))


    ### Used in the other function, could be deleted
    # product = record['fields']['Product']
    # price   = record['fields']['Price']
    # stock   = record['fields']['Stock']

    # print("product: {}, price: {}, stock: {}".format(product, price, stock))

    # #relational lookups
    # merchant_record = record['fields']['Store'][0] #array again

    # vendor_info = at.get('Vendors', record_id=merchant_record, limit=0, offset=None, filter_by_formula=None, view=None, max_records=0, fields=[])['fields']
    # store = vendor_info['Store']
    # group_id =  vendor_info['Groups'][0] # is still in array, could also loop for multiple group assignments
    # group_info = at.get('Location', record_id=group_id, limit=0, offset=None, filter_by_formula=None, view=None, max_records=0, fields=[])['fields']
    # group_name = group_info['Name']

    # print("store: {}, group name: {}".format(store, group_name))

    product = airtable_record_to_json(at, record)
    # print(wcapi.post("products", product).json())
    wcapi.post("products", product).json()
print("done : ) :) :  )")