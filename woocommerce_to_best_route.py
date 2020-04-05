__author__ = "Sonja Peter"
__version__ = "v0.1"
__date___ = "05.04.2020"

# PLEASE USE PYTHON3!

# Import packages
import requests
import json
import geopy
import pandas as pd
import airtable as tab 
import time
import numpy as np


#Connection to woocommerce
from woocommerce import API #https://github.com/woocommerce/wc-api-python

wcapi = API(
    url="https://marchalocal.ch",
    consumer_key= 'ck_7e032301f2b9c73f376bf3f608b7274ca27ce020',
    consumer_secret="cs_6ffda704beefd69e0f771b8bfb01297a53101bf8",
    wp_api=True,
    version="wc/v3",
    timeout=15)

def get_orders_from_woocommerce(API):
    """
    Parameters: 
    -- API: Connection to the woocomerce marchalocal store url="https://marchalocal.ch
    """
    orders = wcapi.get("orders").json()
    orderlist = {}
    for order in orders: 
        address = order['billing']['address_1']
        city = order['billing']['city']
        name = " ".join([order['billing']['first_name'], order['billing']['last_name']])
        order_id = order['id']
        date = order['date_created']
        postcode = order['billing']['postcode']
        products = [x['name'] for x in order['line_items']] #unused product list
        fields = {"name": name, "address": address, "city": city, "postcode": postcode, "products": products, "date": date}
        if not orderlist.get(order_id):
            orderlist[order_id] = fields 
    return orderlist

def address_to_coordinates(address):
    """
    Parameters: 
    -- address: Dictionary of the addresses from the order list taken out of woocomerce
    """
    visits = {}

    # Set the address of your vehicle(s)
    adress_depot = "Post-Passage 9, 4051 Basel"
    locator = geopy.Nominatim(user_agent="myGeocoder")
    location = locator.geocode(adress_depot)
    fleet = {
        "vehicle_1": {
        "start_location": {
            "id": "depot",
            "name": "alte Post",
            "lat": location.latitude,
            "lng": location.longitude
        }
        },
    }

  # Extract the coordinates (lat, long) by geocode from addresses and print if 
  # address can not be found as the routific is a demo file i cannot be larger
  # than 8

 
    for i, key in enumerate(address.keys()): 
        if i > 1600:
            print("[WARNING]\tToo many orders")
            continue
        name = address[key]["name"]
        adresse = address[key]["address"]+", "+address[key]["postcode"]+", "+address[key]["city"] 
        location = locator.geocode(adresse)
        if not location:
            print("[WARNING]\t",adresse,"does not exist")
            continue
        lat= location.latitude
        long= location.longitude
        visits[key] =             {"location" : {
                                          "name": name,
                                          "lat": lat,
                                          "lng": long
                                      }}
        # To not overload the server                   
        time.sleep(0.1)

    # Put together address of vehicles (fleet) and visitis of customer into one 
    # dictionary 
    data = {
        "visits": visits,
        "fleet": fleet
    }

    return data

def order_list_to_shortest_path(orderlist, routific_api_key = "https://api.routific.com/v1/vrp"):
    """
    -- orderlist: Dictionary of coordinates of visits and fleets including name and id
    -- routific_api_key: "https://api.routific.com/v1/vrp"
    """

      #Execute routific

    headers = {
        "Content-Type": "application/json",
        # Trial version valid until 11th of April
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI1ZTg3M2M4Zjc5MGUzZDAwMThjMTczNDYiLCJpYXQiOjE1ODYwOTMyMTR9.VA5jcTaVdJyV3puBt_b4VsvuRjs5LuohKAsgXP682EY"  
        #"Authorization": "bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfaWQiOiI1MzEzZDZiYTNiMDBkMzA4MDA2ZTliOGEiLCJpYXQiOjEzOTM4MDkwODJ9.PR5qTHsqPogeIIe0NyH2oheaGR-SJXDsxPTcUQNq90E"  
      }
    payload = orderlist
    url = routific_api_key
    r = requests.request('POST',url, data = json.dumps(payload), headers= headers)

    # Convert response into a dictonary 
    data = r.json()

    # Number of Coordinates of vehicle 1
    coord_len = len(data['solution']['vehicle_1'])
    coodr = np.zeros((coord_len-1, 2))

    #Make a list of the orders that have to be processed
    list = []
    for i in range(1,len(data['solution']['vehicle_1'])):
        list.append(data['solution']['vehicle_1'][i]['location_id'])

    # Put coordinates into a table (watch out the starting coordinate (hub) are not included)
    coordinates_lat = []
    coordinates_lng = []

    for value in list:
        coordinates_lat.append(orderlist["visits"][int(value)]['location']['lat'])
        coordinates_lng.append(orderlist["visits"][int(value)]['location']['lng'])
    return coordinates_lat,coordinates_lng


if __name__== "__main__":
    ## MAIN ##
    orders = get_orders_from_woocommerce(API)
    addresses = address_to_coordinates(orders)
    coordinates_lat, coordinates_lng= order_list_to_shortest_path(addresses)
    
    #Define a 2D array 
    final_coord = np.zeros((len(coordinates_lat), 2))
    final_coord[:,0] = coordinates_lat
    final_coord[:,1] = coordinates_lng
    
    #Export as csv
    #Path to output !! Please change accordingly !!
    # e.g. path = "/Users/sonjapeter/Desktop/"
    path = ""

    final_coord = pd.DataFrame(final_coord, columns = ["Lat", "Long"])
    final_coord.to_csv(path+"Solution_to_roout_optimization.csv")