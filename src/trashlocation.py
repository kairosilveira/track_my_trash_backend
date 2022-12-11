import os
import pandas as pd
pd.options.mode.chained_assignment = None 
import requests
from urllib.parse import urlencode
import haversine as hs

class TrashLocation:

    API_KEY = os.environ.get("API_KEY")

    def __init__(self, data_type = "json", root_path = None) -> None:
        self.data_type = data_type
        if root_path == None:
            self.root_path = os.path.abspath("")
        else:
            self.root_path = root_path


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

    
    def get_data_path(self, data_file):
        if not isinstance(data_file, str):
            raise ValueError("data_file must be a string")

        data_path = os.path.join(
                        os.path.join(
                            self.root_path,"data"),
                        data_file)  
        self.data_path = data_path
        return data_path


    def get_data(self, data_file):
        '''read the data into a dataFrame'''

        self.get_data_path(data_file)
        df = pd.read_csv(self.data_path)
        self.data = df
        return df

    
    def get_df_of_trash_type(self, trash_type):
        '''
        trash type can be: non_dangereux,dangereux,amiantes
        '''
        df = self.get_data("formatted_data.csv")
        return df[df[trash_type]]

    
    def get_dist_km(self, coords1, coords2):
        dist = hs.haversine((coords1["lat"], coords1["lng"]),(coords2["lat"], coords2["lng"]))
        return dist
        

    def get_n_nearest(self, n, address, trash_type):
        coords = self.get_lat_lng(address)
        df = self.get_df_of_trash_type(trash_type=trash_type)
        array_dist = []
        for lat,lng in zip(df["lat"], df["lng"]):
            dist = hs.haversine((coords["lat"], coords["lng"]),(lat, lng))
            array_dist.append(dist)

        df["dist"] = array_dist
        df_n_nearest = df[["Nom", "formatted_address", "dist"]]
        return df_n_nearest.sort_values("dist").head(n)

if __name__ == "__main__":
    # test code
    local   = TrashLocation()
    address = input("enter your address: ") 
    #address = "rua portugal 1011 bom jardim são jose do rio preto, são paulo"
    df      = local.get_n_nearest(3,address,"amiantes")
    fa      = local.get_formatted_address(address)
    latlng  = local.get_lat_lng(address=address)
    print(latlng)
    print(fa)
    print(df)
 