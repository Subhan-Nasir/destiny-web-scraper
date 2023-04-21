import os
from dotenv import load_dotenv, find_dotenv
import requests
from pprint import pprint
import json
import time

load_dotenv(find_dotenv())



# Bungie membership types:
"""
None: 0
TigerXbox: 1
TigerPsn: 2
TigerSteam: 3
TigerBlizzard: 4
TigerStadia: 5
TigerEgs: 6
TigerDemon: 10
BungieNext: 254
All: -1

"""

start = time.time()

base_url = "https://www.bungie.net/Platform/"
headers = {

    "x-api-key": os.getenv("x-api-key")
}


def get_linked_profiles():
    membership_type = os.getenv("membership_type")
    membership_id = os.getenv("membership_id")

    endpoint = f"Destiny2/{membership_type}/Profile/{membership_id}/LinkedProfiles/"
    url = base_url + endpoint
    payload = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    pprint(response.json())


def get_user_profiles(username, bungie_num=False):
    
    endpoint = f"User/Search/GlobalName/{0}/"
    url = base_url + endpoint

    payload = json.dumps({
    "displayNamePrefix": username
    })
    
    response = requests.post(url, headers=headers, data=payload).json()
    
    if bungie_num:
        filtered_results = next(item for item in response["Response"]["searchResults"] if item["bungieGlobalDisplayNameCode"] == bungie_num)
        print("-"*150)
        print("FILTERED RESULTS")
        pprint(filtered_results)
        print("-"*150)

    print("-"*150)
    print("API RESPONSE:")
    pprint(response)
    print("-"*150)


    return response

def get_user_memberships(username, bungie_num= False):
    memberships = []
    api_response = get_user_profiles(username, bungie_num)
    # pprint(api_response)
    



    for item in api_response["Response"]["searchResults"][0]["destinyMemberships"]:
        id = item["membershipId"]
        membership_type = item["membershipType"]
        memberships.append({"id": id, "type": membership_type})

    return memberships


def get_account_stats(membership_id, membership_type):
    endpoint = f"Destiny2/{membership_type}/Account/{membership_id}/Stats/"
    url = base_url + endpoint

    payload = ""
    response = requests.request("GET", url, headers=headers, data=payload).json()
    return response
    


if __name__ == "__main__":

    memberships = get_user_memberships("Moira", 4231)
    steam_membership = next(item for item in memberships if item["type"] == 3)
    account_stats = get_account_stats(steam_membership["id"], steam_membership["type"])
    
    

    with open('account_stats.json', 'w', encoding='utf-8') as f:
        json.dump(account_stats, f, ensure_ascii=False, indent=4)

    end = time.time()
    print(f"RUNTIME = {round(end-start, 2)}seconds")



