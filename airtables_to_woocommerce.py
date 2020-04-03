'''
fteufel
load records from airtable, reformat and push as product into woocommerce
'''

from airtable import airtable #https://github.com/josephbestjames/airtable.py
from IPython import embed
from woocommerce import API #https://github.com/woocommerce/wc-api-python

API_KEY = 'keyO4pjsHsgtCPofA'
BASE_ID = 'app1fFJJYvoUtSQUL'
TABLE_NAME = 'Inventory'

at = airtable.Airtable(BASE_ID, API_KEY)
table = at.get(TABLE_NAME)
#table = at.get(TABLE_NAME)
#vendors_table = at.get('Vendors')


#super naive implementation, iterate over all records and update
for record in table['records']:
    product = record['fields']['Product']
    price   = record['fields']['Price']
    stock   = record['fields']['Stock']

    #relational lookups
    merchant_record = record['fields']['Store'][0] #array again

    vendor_info = at.get('Vendors', record_id=merchant_record, limit=0, offset=None, filter_by_formula=None, view=None, max_records=0, fields=[])['fields']
    store = vendor_info['Store']
    group_id =  vendor_info['Groups'][0] # is still in array, could also loop for multiple group assignments
    group_info = at.get('Location', record_id=group_id, limit=0, offset=None, filter_by_formula=None, view=None, max_records=0, fields=[])['fields']
    group_name = group_info['Name']

    print(group_name)



wcapi = API(
    url="http://marchalocal.ch",
    consumer_key= 'ck_8239347f0b5b3cf8099e3eff1dc0ef398f23cfa8',
    consumer_secret="cs_3360619c363b5d00a254d6b9636b11a0b5a8c63b",
    version="wc/v3"
)






#delete all IDs that need to be updated
# Force delete example.

wcapi.post("products", data)
print(wcapi.delete("products/100", params={"force": True}).json())

###
def airtable_record_to_json(database, record):
    product = record['fields']['Product']
    price   = record['fields']['Price']
    stock   = record['fields']['Stock']

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
        #"type": "simple",
        "regular_price": price,
        "description": "Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Vestibulum tortor quam, feugiat vitae, ultricies eget, tempor sit amet, ante. Donec eu libero sit amet quam egestas semper. Aenean ultricies mi vitae est. Mauris placerat eleifend leo.",
        "short_description": "Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.",
        "categories": [
            {
                "id": 9
            },
            {
                "id": 14
            }
        "attributes":[
            {
                'name' = 'Store'
                'visible' = True
            },
            {
                'name' = 'Store Group'
                'visible' = True
            }
        ]
        ],
    }


    return data
