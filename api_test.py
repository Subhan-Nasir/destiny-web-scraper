import os
from dotenv import load_dotenv, find_dotenv
import requests
from pprint import pprint

load_dotenv(find_dotenv())
print(os.getenv("x-api-key"))

def get_equipment():
    membership_type = os.getenv("membership_type")
    membership_id = os.getenv("membership_id")
    

    base_url = "https://www.bungie.net/Platform" 
    endpoint = f"/Destiny2/{membership_type}/Profile/{membership_id}/LinkedProfiles/"

    url = base_url + endpoint
    payload = {}

    headers = {

        "x-api-key":os.getenv("x-api-key")
    }
    
    response = requests.request("GET", url, headers=headers, data=payload)
    pprint(response.json())


if __name__ == "__main__":
    get_equipment()
