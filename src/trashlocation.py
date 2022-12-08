import os
import pandas as pd
import requests
from urllib.parse import urlencode

class TrashLocation:

    API_KEY = os.environ.get("API_KEY")

    def __init__(self, data_type = "json") -> None:
        self.data_type = data_type


    def get_url(self, address):
        endpoint = "https://maps.googleapis.com/maps/api/geocode/"
        params = {
            "address":address,
            "key":self.API_KEY
        }
        url_params = urlencode(params)
        url = f"{endpoint}{self.data_type}?{url_params}"
        return url


    def make_request(self, url):
        r = requests.get(url)
        if r.status_code not in range(200,300):
            return {}
        r_json = r.json()
        self.last_json = r_json
        return r_json


    def get_lat_lng(self, address):
        url = self.get_url(address)
        json_response = self.make_request(url)
        lat_lng = json_response["results"][0]['geometry']["location"]
        return lat_lng


    def get_formatted_address(self, address):
        url = self.get_url(address)
        json_response = self.make_request(url)
        formatted_adress = json_response["results"][0]['formatted_address']
        return formatted_adress

if __name__ == "__main__":
    #test code
    locater = TrashLocation()
    address = input("enter your address: ") 
    print(locater.get_lat_lng(address=address))
    print(locater.get_formatted_address(address=address))