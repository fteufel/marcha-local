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